using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using TMPro;

public class CharacterSelectControl : MonoBehaviour
{
    public GameObject PanelGrid;

    [Header("ItemInfo")]
    public GameObject PrefabItem;
    private int _id;

    [Header("CharaterInfo")]
    public Image FullImage;
    public TextMeshProUGUI Name_text;
    public TextMeshProUGUI Info_text;

    private void Start()
    {
        if (PanelGrid.gameObject.transform.childCount != 0)
        {
            for (int i = 0; i < PanelGrid.gameObject.transform.childCount; i++)
            {
                Destroy(PanelGrid.gameObject.transform.GetChild(i).gameObject);
            }
        }
        setupInfo(101);

        ResetItem();
    }

    private void ResetItem()
    {
        foreach (var Itemkey in DataControl.Instance.Characters_DataBase.Keys)
        {
            GameObject Item = Instantiate(PrefabItem, PanelGrid.transform.position, PanelGrid.transform.rotation);
            Item.transform.SetParent(PanelGrid.transform);
            Item.transform.localScale = Vector3.one;
            Item.GetComponent<CharacterSelectItem>().ID = DataControl.Instance.Characters_DataBase[Itemkey].ID;
            Item.GetComponent<CharacterSelectItem>().selectControl = this;
        }
        RectTransform rt = PanelGrid.GetComponent(typeof(RectTransform)) as RectTransform;
        GridLayoutGroup GridLayoit = PanelGrid.GetComponent(typeof(GridLayoutGroup)) as GridLayoutGroup;
        int _isleftcount = DataControl.Instance.Characters_DataBase.Count % 2;

        if (_isleftcount == 0)
            rt.sizeDelta = new Vector2(rt.rect.width, (DataControl.Instance.Characters_DataBase.Count / 2) * (GridLayoit.cellSize.y + GridLayoit.spacing.y) + GridLayoit.padding.top);
        else
            rt.sizeDelta = new Vector2(rt.rect.width, (DataControl.Instance.Characters_DataBase.Count / 2 +1) * (GridLayoit.cellSize.y + GridLayoit.spacing.y) + GridLayoit.padding.top);

    }

    public void setupInfo(int ID)
    {
        string FullImagepath = "CharacterSelect/" + ID + "/FullImage";
        FullImage.sprite = Resources.Load<Sprite>(FullImagepath);
        
        Name_text.text = DataControl.Instance.Characters_DataBase[ID].Name;
        Characters character = DataControl.Instance.Characters_DataBase[ID];
        string Info = string.Empty;

        Info += "生日:" + character.Birth +"\n";
        Info += "星座:" + character.StarSign +"\n";

        #region  Relationship
        string _Relationship = string.Empty;
        if (character.Relationship) 
            _Relationship = "有";
        else
            _Relationship = "無";

        if (ID.ToString().StartsWith("1"))
            Info += "女朋友:" + _Relationship + "\n";
        else
            Info += "男朋友:" + _Relationship + "\n";
        #endregion

        #region Job
        if (character.StartJob != 0)
        { 
            Info += "工作:" + DataControl.Instance.Work_DataBase[character.StartJob].Name + "\n";
            Info += "薪水:" + DataControl.Instance.Work_DataBase[character.StartJob].MonthlySalary + "\n";      
        }
        else
            Info += "工作:無" +"\n";
        #endregion

        Info += "零用錢:" + character.PocketMoney + "\n";
        Info += "月花費:" + character.LivingExpend + "\n";
        Info_text.text = Info;
        _id = ID;
    }

    public void Submmit()
    {
        PlayerDataBase dataBase = new PlayerDataBase();
        Characters character = DataControl.Instance.Characters_DataBase[_id];

        dataBase.Name = character.Name;
        dataBase.PocketMoney = character.PocketMoney;
        dataBase.LivingExpend = character.LivingExpend;
        dataBase.Relationship = character.Relationship;
        dataBase.Birth = character.Birth;


        WorkList workList = new WorkList();
        if (character.StartJob != 0)
        {
            int JobNum = character.StartJob;
            Works work = DataControl.Instance.Work_DataBase[JobNum];

            workList.Name = work.Name;
            workList.Post = work.Post;
            workList.Time = work.MonthlyTime;
            workList.Salary = work.MonthlySalary;
            dataBase.Salary = work.MonthlySalary;
            workList.MonthlyRequire = work.MonthlyRequire;
            dataBase.workList.Add(workList);
        }
        Debug.Log(dataBase.AllocateCash);

        DataControl.Instance._playerData = dataBase;

        SavePlayerData.Save(DataControl.Instance._playerData);
    }
}
