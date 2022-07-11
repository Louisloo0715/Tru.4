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
        Name_text.text = "人物名";
        Info_text.text = "";

        ResetItem();
    }

    void ResetItem()
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
        if (ID.ToString().StartsWith("1"))
            Info += "女朋友:" + character.Relationship + "\n";
        else
            Info += "男朋友:" + character.Relationship + "\n";
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
    }
}
