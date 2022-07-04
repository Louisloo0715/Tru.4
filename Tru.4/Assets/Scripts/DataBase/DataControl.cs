using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DataControl : MonoBehaviour
{
    public static DataControl Instance;

    public int ID;

    [Header("DataBase¸ô®|")]
    public const string CharactersDataBasepath = "DataBase/CharacterDataBase";

    [Header("DataBase")]
    public CharactersDataBase Characters_DataBase;

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
        Characters_DataBase = CharactersDataBase.LoadDataBase(CharactersDataBasepath);
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            foreach (var character in Characters_DataBase.Obj)
            {
                if (character.ID != ID)
                    continue;
                else
                    Debug.LogError(character.ID + " " + character.Name);
                    
            }
        }
    }
}
