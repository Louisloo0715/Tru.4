using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Xml;
using UnityEngine.UI;

public class DataControl : MonoBehaviour
{
    public static DataControl Instance;
    public InputField GetIDInputField;
    public Text ShowDataText;
    private string input;

    public int ID;


    [Header("DataBase路徑")]
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
        Work_DataBase = WorkDataBase.IntoDictionary(Workpath);
        DarkCards_DataBase = DarkCardsDataBase.IntoDictionary(DarkCardspath);
        Characters_DataBase = CharactersDataBase.IntoDictionary(CharactersDataBasepath);
        LargeGreats_DataBase = LargeGreatData.IntoDictionary(LargeGreatpath);
        LittleGreats_DataBase = LittleGreatData.IntoDictionary(LittleGreatpath);
        LittleLuck_DataBase = LittleLuckData.IntoDictionary(LittleLuckpath);
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Debug.Log(Work_DataBase[ID].MonthlySalary);
        }
    }

    public void ReadStringInput(string s)
    {
        input = s;
        Debug.Log(input);
        ShowText();
    }

    public void ShowText()
    {
        string showText = string.Empty;
        int id;
        int.TryParse(input, out id);

        if (!Characters_DataBase.ContainsKey(id))
        {
            ShowDataText.text = "查無此人";
            return;
        }
        showText += "姓名：" + Characters_DataBase[id].Name + "\n";
        showText += "生日：" + Characters_DataBase[id].Birth + "\n";
        showText += "星座：" + Characters_DataBase[id].StarSign + "\n";
        showText += "男/女朋友：" + Characters_DataBase[id].Relationship + "\n";
        showText += "零用錢：" + Characters_DataBase[id].PocketMoney + "\n";

        if (Characters_DataBase[id].StartJob == 0)
            showText += "每月薪水： 0\n";
        else
            showText += "每月薪水：" + Work_DataBase[Characters_DataBase[id].StartJob].MonthlySalary + "\n";

        showText += "每個月生活支出：" + Characters_DataBase[id].LivingExpend + "\n";

        if (Characters_DataBase[id].StartJob == 0)
            showText += "初始工作： 無工作\n";
        else
            showText += "工作地：" + Work_DataBase[Characters_DataBase[id].StartJob].Name + "\n";


        if (Characters_DataBase[id].StartJob == 0)
            showText += "每個月可支配金額：" + Characters_DataBase[id].AllocateCash + "\n";
        else
        {
            int sum = Characters_DataBase[id].AllocateCash;
            showText += "每個月可支配金額：" + sum +"\n";
        }

        showText += "每個月可支配時間：" + Characters_DataBase[id].AllocateTime + "\n";

        ShowDataText.text = showText;
    }
}
