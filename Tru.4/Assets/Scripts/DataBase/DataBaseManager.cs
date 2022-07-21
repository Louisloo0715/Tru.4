using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Xml.Serialization;
using System.IO;

#region 角色資料
[XmlRoot("CharactersData")]
public class CharactersDataBase
{
    [XmlArray("Characters")]
    [XmlArrayItem("Character")]
    public List<Characters> Obj = new List<Characters>();
    /// <summary>
    /// 載入角色資料的Xml檔
    /// </summary>
    /// <param name="path"></param>
    /// <returns></returns>
    public static CharactersDataBase LoadDataBase(string path)
    {
        TextAsset _xml = Resources.Load<TextAsset>(path);
        XmlSerializer serializer = new XmlSerializer(typeof(CharactersDataBase));
        StringReader reader = new StringReader(_xml.text);
        CharactersDataBase Obj = new CharactersDataBase();
        Obj = serializer.Deserialize(reader) as CharactersDataBase;
        reader.Close();
        return Obj;
    }

    public static Dictionary<int, Characters> IntoDictionary(string path)
    {
        Dictionary<int, Characters> temp = new Dictionary<int, Characters>();
        foreach (var obj in LoadDataBase(path).Obj)
        {
            temp.Add(obj.ID, obj);
        }
        return temp;
    }
}

public class Characters
{

    [XmlAttribute("Character")]
    public string InteractiveObj;

    /// <summary>
    /// 角色ID(男性1開頭，女性2開頭)
    /// </summary>
    [XmlElement("ID")]
    public int ID;

    /// <summary>
    /// 角色名稱
    /// </summary>
    [XmlElement("Name")]
    public string Name;

    /// <summary>
    /// 遊戲角色生日
    /// </summary>
    [XmlElement("Birth")]
    public string Birth;

    /// <summary>
    /// 遊戲角色星座
    /// </summary>
    [XmlElement("StarSign")]
    public string StarSign;

    /// <summary>
    /// 有無男女朋友
    /// </summary>
    [XmlElement("Relationship")]
    public bool Relationship;

    /// <summary>
    /// 零用錢
    /// </summary>
    [XmlElement("PocketMoney")]
    public int PocketMoney;

    /// <summary>
    /// 初始工作薪資
    /// </summary>
    [XmlElement("Salary")]
    private int salary;
    public int Salary
    {
        get { return salary; }
        set
        {
            if (StartJob != 0)
                salary = DataControl.Instance.Work_DataBase[StartJob].MonthlySalary;
            else
                salary = 0;
        }
    }

    /// <summary>
    /// 每月固定支出
    /// </summary>
    [XmlElement("LivingExpend")]
    public int LivingExpend;

    /// <summary>
    /// 初始工作ID
    /// </summary>
    [XmlElement("StartJob")]
    public int StartJob;

    [XmlElement("AllocateCash")]
    private int allocateCash;
    /// <summary>
    /// 可支配金額
    /// </summary>
    public int AllocateCash
    {
        get { return allocateCash; }
        set
        {
            allocateCash = (PocketMoney + Salary) - LivingExpend;
        }
    }

    [XmlElement("AllocateTime")]
    private int allcateTime;
    /// <summary>
    /// 可支配時間
    /// </summary>
    public int AllocateTime
    {
        get { return allcateTime; }
        set
        {
            if (StartJob != 0)
                allcateTime = value - DataControl.Instance.Work_DataBase[StartJob].MonthlyTime;
            else
                allcateTime = value;
        }
    }

}
#endregion

#region 黑暗卡資料
[XmlRoot("DarkCards")]
public class DarkCardsDataBase
{
    [XmlArray("Cards")]
    [XmlArrayItem("Card")]
    public List<DarkCards> Obj = new List<DarkCards>();

    /// <summary>
    /// 載入黑暗卡的Xml檔
    /// </summary>
    /// <param name="path"></param>
    /// <returns></returns>
    public static DarkCardsDataBase LoadDataBase(string path)
    {
        TextAsset _xml = Resources.Load<TextAsset>(path);
        XmlSerializer serializer = new XmlSerializer(typeof(DarkCardsDataBase));
        StringReader reader = new StringReader(_xml.text);
        DarkCardsDataBase Obj = new DarkCardsDataBase();
        Obj = serializer.Deserialize(reader) as DarkCardsDataBase;
        reader.Close();
        return Obj;
    }

    public static Dictionary<int, DarkCards> IntoDictionary(string path)
    {
        Dictionary<int, DarkCards> temp = new Dictionary<int, DarkCards>();
        foreach (var obj in LoadDataBase(path).Obj)
        {
            temp.Add(obj.ID, obj);
        }
        return temp;
    }
}

public class DarkCards
{
    [XmlAttribute("Card")]
    public string Card;

    [XmlElement("ID")]
    public int ID;

    /// <summary>
    /// 懲罰時間
    /// </summary>
    [XmlElement("PunishTime")]
    public int PunishTime;

    /// <summary>
    /// 懲罰金額
    /// </summary>
    [XmlElement("PunishCash")]
    public int PunishCash;

    /// <summary>
    /// 停賽次數
    /// </summary>
    [XmlElement("Suspended")]
    public int Suspended;

    /// <summary>
    /// 黑暗卡內容描述
    /// </summary>
    [XmlElement("Description")]
    public string Description;

    /// <summary>
    /// 是否有無其餘條件
    /// </summary>
    [XmlElement("OtherRequire")]
    public bool OtherRequire;

}
#endregion

//可支配所得>6000強制大爽 剩餘皆小爽
# region 大爽卡資料
[XmlRoot("LargeGreatData")]
public class LargeGreatData
{
    [XmlArray("LargeGreats")]
    [XmlArrayItem("LargeGreat")]
    public List<LargeGreatCard> Obj = new List<LargeGreatCard>();

    public static LargeGreatData LoadDataBase(string path)
    {
        TextAsset _xml = Resources.Load<TextAsset>(path);
        XmlSerializer serializer = new XmlSerializer(typeof(LargeGreatData));
        StringReader reader = new StringReader(_xml.text);
        LargeGreatData Obj = serializer.Deserialize(reader) as LargeGreatData;
        reader.Close();
        return Obj;
    }

    public static Dictionary<int, LargeGreatCard> IntoDictionary(string path)
    {
        Dictionary<int, LargeGreatCard> temp = new Dictionary<int, LargeGreatCard>();
        foreach (var obj in LoadDataBase(path).Obj)
        {
            temp.Add(obj.ID, obj);
        }
        return temp;
    }
}

public class LargeGreatCard
{
    [XmlAttribute("LargeGreat")]
    public string LargeGreat;

    [XmlElement("ID")]
    public int ID;

    /// <summary>
    /// 大爽卡物件名稱
    /// </summary>
    [XmlElement("Name")]
    public string Name;

    /// <summary>
    /// 總金額(用於一次給付)
    /// </summary>
    [XmlElement("TotalCash")]
    public int TotalCash;

    /// <summary>
    /// 是否可分期
    /// </summary>
    [XmlElement("Installment")]
    public bool Installment;

    /// <summary>
    /// 共分期幾月
    /// </summary>
    [XmlElement("MonthToPay")]
    public int MonthToPay;

    /// <summary>
    /// 分期後每月需支付金額
    /// </summary>
    [XmlElement("CashPerMonth")]
    public int CashPerMonth;

    /// <summary>
    /// 大爽卡內容描述
    /// </summary>
    [XmlElement("Description")]
    public string Description;

    /// <summary>
    /// 人脈點數增加
    /// </summary>
    [XmlElement("ConnectionPoint")]
    public int ConnectionPoint;
    
    /// <summary>
    /// 是否有無其條件
    /// </summary>
    [XmlElement("OtherRequire")]
    public bool OtherRequire;
}
#endregion

# region 小爽卡資料
[XmlRoot("LittleGreatData")]
public class LittleGreatData
{
    [XmlArray("LittleGreats")]
    [XmlArrayItem("LittleGreat")]
    public List<LittleGreatCard> Obj = new List<LittleGreatCard>();

    public static LittleGreatData LoadDataBase(string path)
    {
        TextAsset _xml = Resources.Load<TextAsset>(path);
        XmlSerializer serializer = new XmlSerializer(typeof(LittleGreatData));
        StringReader reader = new StringReader(_xml.text);
        LittleGreatData Obj = serializer.Deserialize(reader) as LittleGreatData;
        reader.Close();
        return Obj;
    }

    public static Dictionary<int, LittleGreatCard> IntoDictionary(string path)
    {
        Dictionary<int, LittleGreatCard> temp = new Dictionary<int, LittleGreatCard>();
        foreach (var obj in LoadDataBase(path).Obj)
        {
            temp.Add(obj.ID, obj);
        }
        return temp;
    }

}

public class LittleGreatCard
{
    [XmlAttribute("LittleGreat")]
    public string LittleGreat;

    [XmlElement("ID")]
    public int ID;

    /// <summary>
    /// 需支付總金額
    /// </summary>
    [XmlElement("TotalCash")]
    public int TotalCash;

    /// <summary>
    /// 可獲得之人脈點數
    /// </summary>
    [XmlElement("ConnectionPoint")]
    public int ConnectionPoint;

    /// <summary>
    /// 需花費的總時間
    /// </summary>
    [XmlElement("TotalTime")]
    public int TotalTime;

    /// <summary>
    /// 小爽卡內容描述
    /// </summary>
    [XmlElement("Description")]
    public string Description;
    
    /// <summary>
    /// 持續時間
    /// </summary>
    [XmlElement("ContinuedTime")]
    public int ContinuedTime;

    /// <summary>
    /// 是否有無其餘條件
    /// </summary>
    [XmlElement("OtherRequire")]
    public bool OtherRequire;

}
#endregion

#region 好運卡資料
[XmlRoot("LittleLuckData")]
public class LittleLuckData
{
    [XmlArray("LittleLucks")]
    [XmlArrayItem("LittleLuck")]
    public List<LittleLuckCard> Obj = new List<LittleLuckCard>();

    public static LittleLuckData LoadDataBase(string path)
    {
        TextAsset _xml = Resources.Load<TextAsset>(path);
        XmlSerializer serializer = new XmlSerializer(typeof(LittleLuckData));
        StringReader reader = new StringReader(_xml.text);
        LittleLuckData Obj = serializer.Deserialize(reader) as LittleLuckData;
        reader.Close();
        return Obj;
    }

    public static Dictionary<int, LittleLuckCard> IntoDictionary(string path)
    {
        Dictionary<int, LittleLuckCard> temp = new Dictionary<int, LittleLuckCard>();
        foreach (var obj in LoadDataBase(path).Obj)
        {
            temp.Add(obj.ID, obj);
        }
        return temp;
    }
}

public class LittleLuckCard
{
    [XmlAttribute("LittleLuck")]
    public string LittleLuck;

    [XmlElement("ID")]
    public int ID;

    /// <summary>
    /// 可獲得之總金額
    /// </summary>
    [XmlElement("TotalCash")]
    public int TotalCash;

    /// <summary>
    /// 所需的書本數
    /// </summary>
    [XmlElement("BookNeeds")]
    public int BookNeeds;

    /// <summary>
    /// 所需的人脈點數數
    /// </summary>
    [XmlElement("RelationshipPointNeeds")]
    public int RelationshipPointNeeds;

    /// <summary>
    /// 是否有無其餘條件
    /// </summary>
    [XmlElement("OtherRequire")]
    public bool OtherRequire;

}
#endregion

#region 工作資料
[XmlRoot("WorkDataBase")]
public class WorkDataBase
{
    [XmlArray("Works")]
    [XmlArrayItem("Work")]
    public List<Works> Obj = new List<Works>();

    public static WorkDataBase LoadDataBase(string path)
    {
        TextAsset _xml = Resources.Load<TextAsset>(path);
        XmlSerializer serializer = new XmlSerializer(typeof(WorkDataBase));
        StringReader reader = new StringReader(_xml.text);
        WorkDataBase Obj = serializer.Deserialize(reader) as WorkDataBase;
        reader.Close();
        return Obj;
    }

    public static Dictionary<int, Works> IntoDictionary(string path)
    {
        Dictionary<int, Works> temp = new Dictionary<int, Works>();
        foreach (var obj in LoadDataBase(path).Obj)
        {
            temp.Add(obj.ID, obj);
        }
        return temp;
    }
}

public class Works
{
    [XmlAttribute("Work")]
    public string Work;

    [XmlElement("ID")]
    public int ID;

    /// <summary>
    /// 機構名稱
    /// </summary>
    [XmlElement("Name")]
    public string Name;

    /// <summary>
    /// 職位名稱
    /// </summary>
    [XmlElement("Post")]
    public string Post;

    /// <summary>
    /// 所需人數
    /// </summary>
    [XmlElement("PersonRequire")]
    public int PersonRequire;

    /// <summary>
    /// 初始工作月
    /// </summary>
    [XmlElement("StartMonth")]
    public int StartMonth;

    /// <summary>
    /// 離職月份
    /// </summary>
    [XmlElement("EndMonth")]
    public int EndMonth;

    /// <summary>
    /// 當前時薪價格(可更改)
    /// </summary>
    private double hourlySalary = 168;
    [XmlElement("HourlySalary")]
    public double HourlySalary
    {
        get { return hourlySalary; }
        set { hourlySalary *= value; }
    }

    /// <summary>
    /// 周時
    /// </summary>
    [XmlElement("WeeklyTime")]
    public int WeeklyTime;

    [XmlElement("MonthlySalary")]
    private int monthlySalary;
    /// <summary>
    /// 月薪(時薪 * 月時)
    /// </summary>
    public int MonthlySalary
    {
        get { return monthlySalary; }
        set
        {
            if (monthlySalary == 0)
                monthlySalary = (int)HourlySalary * MonthlyTime;
            else
                monthlySalary = value;
        }
    }

    /// <summary>
    /// 月時
    /// </summary>
    [XmlElement("MonthlyTime")]
    public int MonthlyTime;

    /// <summary>
    /// 年薪
    /// </summary>
    [XmlElement("AnnualSalary")]
    private int annualSalary;
    public int AnnualSalary
    {
        get { return annualSalary; }
        set
        {
            annualSalary = MonthlySalary * 12;
        }
    }

    /// <summary>
    /// 基本月數要求
    /// </summary>
    [XmlElement("MonthlyRequire")]
    public int MonthlyRequire;

    /// <summary>
    /// 是否有無其餘要求
    /// </summary>
    [XmlElement("OtherRequire")]
    public bool OtherRequire;

    /// <summary>
    /// 工作卡內容描述
    /// </summary>
    [XmlElement("Description")]
    public string Description;
}
#endregion

#region 學習卡資料
[XmlRoot("LearningCardData")]
public class LearningCardDataBase
{
    [XmlArray("LearningCards")]
    [XmlArrayItem("LearningCard")]
    public List<LearningCards> Obj = new List<LearningCards>();

    public static LearningCardDataBase LoadDataBase(string path)
    {
        TextAsset _xml = Resources.Load<TextAsset>(path);
        XmlSerializer serializer = new XmlSerializer(typeof(LearningCardDataBase));
        StringReader reader = new StringReader(_xml.text);
        LearningCardDataBase Obj = new LearningCardDataBase();
        Obj = serializer.Deserialize(reader) as LearningCardDataBase;
        reader.Close();
        return Obj;
    }

    public static Dictionary<int, LearningCards> IntoDictionary(string path)
    {
        Dictionary<int, LearningCards> temp = new Dictionary<int, LearningCards>();
        foreach (var obj in LoadDataBase(path).Obj)
        {
            temp.Add(obj.ID, obj);
        }
        return temp;
    }
}

public class LearningCards
{
    [XmlAttribute("Card")]
    public string Card;

    [XmlElement("ID")]
    public int ID;

    /// <summary>
    /// 學習種類(Excel上有備註)
    /// </summary>
    [XmlElement("Type")]
    public int Type;

    /// <summary>
    /// 學習名稱
    /// </summary>
    [XmlElement("Name")]
    public string Name;

    /// <summary>
    /// 獲得書本數
    /// </summary>
    [XmlElement("BookNums")]
    public int BookNums;

    /// <summary>
    /// 需花費總金額
    /// </summary>
    [XmlElement("TotalCash")]
    public string TotalCash;

    /// <summary>
    /// 是否可以全員參與
    /// </summary>
    [XmlElement("PersonRequire")]
    public bool PersonRequire;

    /// <summary>
    /// 可使用次數(0不限次數)
    /// </summary>
    [XmlElement("UseTime")]
    public int UseTime;

    /// <summary>
    /// 每周花費時間
    /// </summary>
    [XmlElement("WeeklyTime")]
    public int WeeklyTime;

    /// <summary>
    /// 每月花費時間
    /// </summary>
    [XmlElement("MonthlyTime")]
    public int MonthlyTime;

    /// <summary>
    /// 獲得人脈點數
    /// </summary>
    [XmlElement("ConnectionPoint")]
    public int ConnectionPoint;

    /// <summary>
    /// 懲罰人脈點數
    /// </summary>
    [XmlElement("Punish_ConnectionPoint")]
    public int Punish_ConnectionPoint;

    /// <summary>
    /// 所需時間(-1持續至遊戲結束)
    /// </summary>
    [XmlElement("MonthNeeds")]
    public int MonthNeeds;

    /// <summary>
    /// 學習卡內容描述
    /// </summary>
    [XmlElement("Description")]
    public string Description;

    /// <summary>
    /// 是否有無其餘條件
    /// </summary>
    [XmlElement("OtherRequire")]
    public bool OtherRequire;

}
#endregion

#region 玩家資訊

[System.Serializable]
public class PlayerDataBase
{
    /// <summary>
    /// 玩家姓名
    /// </summary>
    public string PlayerName = string.Empty;
    /// <summary>
    /// 角色參數
    /// </summary>
    public string Name = string.Empty;
    public bool Gender;
    /// <summary>
    /// 有無男女朋友 
    /// </summary>
    public bool Relationship;
    public string Birth = string.Empty;
    /// <summary>
    /// 零用錢
    /// </summary>
    public int PocketMoney;
    /// <summary>
    /// 每月固定生活支出
    /// </summary>
    public int LivingExpend;
    /// <summary>
    /// 當月額外支出(月初歸零)
    /// </summary>
    public int Expending = 0;
    /// <summary>
    /// 人脈點(預設30點)
    /// </summary>
    public int ConnectionPoint = 30;
    /// <summary>
    /// 暫停遊戲資格次數
    /// </summary>
    public int Suspended = 0;
    public List<WorkList> workList = new List<WorkList>();
    public List<Staging> stagings = new List<Staging>();
    /// <summary>
    /// 當前擁有的書籍數(累積制)
    /// </summary>
    public int BookNum = 0;
    /// <summary>
    /// 用於儲存所有工資所得
    /// </summary>
    public int Salary;

    /// <summary>
    /// 計算當月可支配金額((零用錢 + 總薪資) - 每月固定支出 - 當月額外支出)
    /// </summary>
    /// <returns></returns>
    private int SetallocateCash()
    {
        return (PocketMoney + Salary) - LivingExpend - Expending;
    }

    /// <summary>
    /// 當月可支配金額
    /// </summary>
    public int AllocateCash
    {
        get { return SetallocateCash(); }
        set { }
    }

    /// <summary>
    /// 當月可支配時間(預設200)
    /// </summary>
    public int AllocateTime = 200;

}


/// <summary>
/// 工作列表
/// </summary>
[System.Serializable]
public class WorkList
{
    public int ID;
    public string Name = string.Empty;
    /// <summary>
    /// 職位名稱
    /// </summary>
    public string Post = string.Empty;
    /// <summary>
    /// 是否正在工作中，預設值為True
    /// </summary>
    public bool OnWork = true;
    public int Time;
    public int Salary;
    /// <summary>
    /// 工作月數需求(-1：角色自帶不可辭職)
    /// </summary>
    public int MonthlyRequire;
}

[System.Serializable]
public class ActivityList
{

}

/// <summary>
/// 分期付款(大爽卡使用)
/// </summary>
[System.Serializable]
public class Staging
{
    /// <summary>
    /// 直到遊戲結束(預設為False)
    /// </summary>
    public bool TotheEndOfGame = false;
    public string Name = string.Empty;
    /// <summary>
    /// 每月所需支付
    /// </summary>
    public int CashPerMonth = 0;
    /// <summary>
    /// 剩餘月份
    /// </summary>
    public int LeftMonth = 0;
}

#endregion