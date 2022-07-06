using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Xml;

public class DataControl : MonoBehaviour
{
    public static DataControl Instance;
    public string PlayerName;
    public int CID;
    public int ID;

    [Header("DataBase���|")]
    public const string CharactersDataBasepath = "DataBase/CharacterDataBase";
    public const string DarkCardspath = "DataBase/DarkCardsDataBase";
    public const string LargeGreatpath = "DataBase/LargeGreatDataBase";
    public const string LittleGreatpath = "DataBase/LittleGreatDataBase";
    public const string LittleLuckpath = "DataBase/LittleLuckDataBase";
    public const string Workpath = "DataBase/WorkDataBase";

    [Header("DataBase")]
    public Dictionary<int, Characters> Characters_DataBase = new Dictionary<int, Characters>();
    public Dictionary<int, DarkCards> DarkCards_DataBase = new Dictionary<int, DarkCards>();
    public Dictionary<int, LargeGreatCard> LargeGreats_DataBase = new Dictionary<int, LargeGreatCard>();
    public Dictionary<int, LittleGreatCard> LittleGreats_DataBase = new Dictionary<int, LittleGreatCard>();
    public Dictionary<int, LittleLuckCard> LittleLuck_DataBase = new Dictionary<int, LittleLuckCard>();
    public Dictionary<int, Works> Work_DataBase = new Dictionary<int, Works>();

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
        DarkCards_DataBase = DarkCardsDataBase.IntoDictionary(DarkCardspath);
        Characters_DataBase = CharactersDataBase.IntoDictionary(CharactersDataBasepath);
        LargeGreats_DataBase = LargeGreatData.IntoDictionary(LargeGreatpath);
        LittleGreats_DataBase = LittleGreatData.IntoDictionary(LittleGreatpath);
        LittleLuck_DataBase = LittleLuckData.IntoDictionary(LittleLuckpath);
        Work_DataBase = WorkDataBase.IntoDictionary(Workpath);
    }

    private void Update()
    {
    }
}
