using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Tesr : MonoBehaviour
{
    public Button GirlButton;
    public Button BoyButton;

    public bool isBoy = false;

    private int girlNum;
    private int boyNum;

    public Image image;

    public Text ShowDataText;

    private DataControl instance = new DataControl();

    private void Start()
    {
        instance = DataControl.Instance;
        girlNum = 201;
        boyNum = 101;
        image.sprite = GetSpirt(girlNum);
        ShowText(girlNum);
    }

    public void TurntoGirl()
    {
        image.sprite = GetSpirt(girlNum);
        ShowText(girlNum);
        isBoy = false;
    }

    public void TurntoBoy()
    {
        image.sprite = GetSpirt(boyNum);
        ShowText(boyNum);
        isBoy = true;
    }

    public void UpdataLeft()
    {
        if (isBoy)
        {
            boyNum--;

            if (boyNum <= 101)
                boyNum = 101;
            else if (boyNum >= 110)
                boyNum = 110;
            image.sprite = GetSpirt(boyNum);
            ShowText(boyNum);
        }
        else
        {
            girlNum--;
            if (girlNum <= 201)
                girlNum = 201;
            else if (girlNum >= 210)
                girlNum = 210;
            image.sprite = GetSpirt(girlNum);
            ShowText(girlNum);
        }
    }

    public void UpdataRight()
    {
        if (isBoy)
        {
            boyNum++;
            if (boyNum <= 101)
                boyNum = 101;
            else if (boyNum >= 110)
                boyNum = 110;
            image.sprite = GetSpirt(boyNum);
            ShowText(boyNum);
        }
        else
        {
            girlNum++;
            if (girlNum <= 201)
                girlNum = 201;
            else if (girlNum >= 210)
                girlNum = 210;
            image.sprite = GetSpirt(girlNum);
            ShowText(girlNum);
        }
    }

    private Sprite GetSpirt(int ID)
    {
        Sprite sprite = Resources.Load<Sprite>("CharacterImage/" + instance.Characters_DataBase[ID].Name);
        return sprite;
    }

    public void ShowText(int id)
    {
        string showText = string.Empty;

        if (!instance.Characters_DataBase.ContainsKey(id))
        {
            ShowDataText.text = "查無此人";
            return;
        }
        showText += "姓名：" + instance.Characters_DataBase[id].Name + "\n";
        showText += "生日：" + instance.Characters_DataBase[id].Birth + "\n";
        showText += "星座：" + instance.Characters_DataBase[id].StarSign + "\n";
        showText += "男/女朋友：" + instance.Characters_DataBase[id].Relationship + "\n";
        showText += "零用錢：" + instance.Characters_DataBase[id].PocketMoney + "\n";

        if (instance.Characters_DataBase[id].StartJob == 0)
            showText += "每月薪水： 0\n";
        else
            showText += "每月薪水：" + instance.Work_DataBase[instance.Characters_DataBase[id].StartJob].MonthlySalary + "\n";

        showText += "每個月生活支出：" + instance.Characters_DataBase[id].LivingExpend + "\n";

        if (instance.Characters_DataBase[id].StartJob == 0)
            showText += "初始工作： 無工作\n";
        else
            showText += "工作地：" + instance.Work_DataBase[instance.Characters_DataBase[id].StartJob].Name + "\n";


        if (instance.Characters_DataBase[id].StartJob == 0)
            showText += "每個月可支配金額：" + instance.Characters_DataBase[id].AllocateCash + "\n";
        else
        {
            int sum = instance.Characters_DataBase[id].AllocateCash;
            showText += "每個月可支配金額：" + sum + "\n";
        }

        showText += "每個月可支配時間：" + instance.Characters_DataBase[id].AllocateTime + "\n";

        ShowDataText.text = showText;
    }

    public void commitPlayer()
    {
        if (isBoy)
            DataControl.Instance.ID = boyNum;
        else
            DataControl.Instance.ID = girlNum;
    }
}
