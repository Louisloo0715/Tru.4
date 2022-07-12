using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Xml;
using UnityEngine.UI;

public class DataControl : MonoBehaviour
{
    public static DataControl Instance;

    [Header("玩家參數")]
    [SerializeField]
    private PlayerDataBase PlayerData = new PlayerDataBase();
    public PlayerDataBase _playerData 
    {
        get { return PlayerData; }
        set { PlayerData = value; }
    }



    public TextMesh ShowDataText;
    private string input;

    public int ID;

    #region 所有路徑
    [Header("DataBase路徑")]
    public const string CharactersDataBasepath = "DataBase/CharacterDataBase";
    public const string DarkCardspath = "DataBase/DarkCardsDataBase";
    public const string LargeGreatpath = "DataBase/LargeGreatDataBase";
    public const string LittleGreatpath = "DataBase/LittleGreatDataBase";
    public const string LittleLuckpath = "DataBase/LittleLuckDataBase";
    public const string Workpath = "DataBase/WorkDataBase";
    #endregion

    #region 所有DataBase
    [Header("DataBase")]
    public Dictionary<int, Characters> Characters_DataBase = new Dictionary<int, Characters>();
    public Dictionary<int, DarkCards> DarkCards_DataBase = new Dictionary<int, DarkCards>();
    public Dictionary<int, LargeGreatCard> LargeGreats_DataBase = new Dictionary<int, LargeGreatCard>();
    public Dictionary<int, LittleGreatCard> LittleGreats_DataBase = new Dictionary<int, LittleGreatCard>();
    public Dictionary<int, LittleLuckCard> LittleLuck_DataBase = new Dictionary<int, LittleLuckCard>();
    public Dictionary<int, Works> Work_DataBase = new Dictionary<int, Works>();
    #endregion

    #region Singleton
    private void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(this);
    }
    #endregion

    void Start()
    {
        Work_DataBase = WorkDataBase.IntoDictionary(Workpath);
        DarkCards_DataBase = DarkCardsDataBase.IntoDictionary(DarkCardspath);
        Characters_DataBase = CharactersDataBase.IntoDictionary(CharactersDataBasepath);
        LargeGreats_DataBase = LargeGreatData.IntoDictionary(LargeGreatpath);
        LittleGreats_DataBase = LittleGreatData.IntoDictionary(LittleGreatpath);
        LittleLuck_DataBase = LittleLuckData.IntoDictionary(LittleLuckpath);
        randomID();
    }

    private void Update()
    {
    }

    void randomID()
    {
        int ran = Random.Range(1, 16);
        ShowDataText.text = DarkCards_DataBase[ran].Description;
        ShowDataText.text = ShowDataText.text.Replace("\\n", "\n");;
    } 
    
}

