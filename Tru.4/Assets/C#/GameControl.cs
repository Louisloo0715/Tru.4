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

        whoWinsTextShadow = GameObject.Find("WhoWinsText");
        player1MoveText = GameObject.Find("Player1MoveText");
        player2MoveText = GameObject.Find("Player2MoveText");


        GameObject[] players = GameObject.FindGameObjectsWithTag("Player");
        for (int i = 0; i < players.Length; i++)
        {
            Players.Add(i + 1, players[i]);
            playerStartWaypoint.Add(0);
        }



        whoWinsTextShadow.gameObject.SetActive(false);
        player1MoveText.gameObject.SetActive(true);
        player2MoveText.gameObject.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        if (Players[playerTurnNum].GetComponent<FollowThePath>().waypointIndex > playerStartWaypoint[playerTurnNum-1] + diceSideThrown)
        {
            Players[playerTurnNum].GetComponent<FollowThePath>().moveAllowed = false;
            playerStartWaypoint[playerTurnNum-1] = Players[playerTurnNum].GetComponent<FollowThePath>().waypointIndex - 1;
        }

        if (Players[playerTurnNum].GetComponent<FollowThePath>().waypointIndex == Players[playerTurnNum].GetComponent<FollowThePath>().waypoints.Length)
        {
            playerStartWaypoint[playerTurnNum - 1] = 0;
        }
    }

    public void MovePlayer(int playerToMove)
    {
        Players[playerToMove].GetComponent<FollowThePath>().moveAllowed = true;
        playerTurnNum = playerToMove;
    }
}
