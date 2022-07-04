using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Xml;

public class DataControl : MonoBehaviour
{
    public static DataControl Instance;
    public string PlayerName;
    public int ID;

    [Header("DataBase¸ô®|")]
    public const string CharactersDataBasepath = "DataBase/CharacterDataBase";
    public const string JobDataBasepath = "DataBase/JobDataBase";
    public const string DarkCardspath = "DataBase/DarkCardsDataBase";

    [Header("DataBase")]
    public CharactersDataBase Characters_DataBase;
    public JobsExperience Jobs_DataBase;
    public DarkCardsDataBase DarkCards_DataBase;

    #region Singleton
    private void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(this);
    }
    #endregion

    private void Start()
    {
        DarkCards_DataBase = DarkCardsDataBase.LoadDataBase(DarkCardspath);
        Characters_DataBase = CharactersDataBase.LoadDataBase(CharactersDataBasepath);
        Jobs_DataBase = JobsExperience.LoadDataBase(JobDataBasepath);
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            while(DarkCards_DataBase.Obj.Count != 0)
                DarkCards_DataBase = DarkCardsDataBase.LoadDataBase(DarkCardspath);
            foreach (var job in DarkCards_DataBase.Obj)
            {
                if (job.ID != ID)
                    continue;
                else
                    Debug.Log(job.PunishCash);
            }
       }
    }
}
