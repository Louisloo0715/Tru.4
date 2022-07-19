using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;

public class GameControl : MonoBehaviour
{

    private static GameObject whoWinsTextShadow, player1MoveText, player2MoveText;

    public Dictionary<int, GameObject> Players = new Dictionary<int, GameObject>();
    [SerializeField]
    private List<int> playerStartWaypoint = new List<int>();
    [SerializeField]
    private int playerTurnNum = 1;

    public static int diceSideThrown = 0;

    public static bool gameOver = false;

    public static GameControl Instance;
    private void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(this);
    }

    // Use this for initialization
    void Start()
    {
        #region 收集當前場景上的玩家並初始化每位玩家的路徑點
        GameObject[] players = GameObject.FindGameObjectsWithTag("Player");
        for (int i = 0; i < players.Length; i++)
        {
            Players.Add(i + 1, players[i]);
            playerStartWaypoint.Add(0);
        }
        #endregion
    }

    // Update is called once per frame
    void Update()
    {
        //當(玩家已經過的路徑點)大於(擲到的點數+移動前已經過的路徑點)時，換下一位玩家
        if (Players[playerTurnNum].GetComponent<FollowThePath>().waypointIndex > playerStartWaypoint[playerTurnNum - 1] + diceSideThrown)
        {
            //目前玩家停止行動
            Players[playerTurnNum].GetComponent<FollowThePath>().moveAllowed = false;
            playerStartWaypoint[playerTurnNum - 1] = Players[playerTurnNum].GetComponent<FollowThePath>().waypointIndex - 1;
            //執行當前位置事件
            Players[playerTurnNum].GetComponent<FollowThePath>().waypoints[playerStartWaypoint[playerTurnNum - 1]].GetComponent<EventSystem>().DoEvent(Players[playerTurnNum].GetComponent<PlayerData>());

            StartCoroutine(PlayerSuspended());
        }

        if (Players[playerTurnNum].GetComponent<FollowThePath>().waypointIndex == Players[playerTurnNum].GetComponent<FollowThePath>().waypoints.Length)
        {
            playerStartWaypoint[playerTurnNum - 1] = 0;
        }
    }

    public void MovePlayer()//將當前玩家變為可行動的
    {
        Players[playerTurnNum].GetComponent<FollowThePath>().moveAllowed = true;
    }

    IEnumerator PlayerSuspended()
    {
        ChangPlayer();

        if (Players[playerTurnNum].GetComponent<PlayerData>()._playerData.Suspended != 0)
        {
            Players[playerTurnNum].GetComponent<PlayerData>()._playerData.Suspended--;
            yield return new WaitForSeconds(1f);
            ChangPlayer();
        }
        else
            yield return new WaitForSeconds(1f);

    }

    private void ChangPlayer()
    {
        if (playerTurnNum != Players.Count)
            playerTurnNum++;
        else
            playerTurnNum = 1;
    }
}
