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

    [XmlElement("ID")]
    public int ID;

    [XmlElement("Name")]
    public string Name;

    [XmlElement("Birth")]
    public string Birth;

    [XmlElement("StarSign")]
    public string StarSign;

    [XmlElement("Relationship")]
    public bool Relationship;

    [XmlElement("PocketMoney")]
    public int PocketMoney;

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

    [XmlElement("LivingExpend")]
    public int LivingExpend;

    [XmlElement("StartJob")]
    public int StartJob;

    [XmlElement("AllocateCash")]
    private int allocateCash;
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

    [XmlElement("PunishTime")]
    public int PunishTime;

    [XmlElement("PunishCash")]
    public int PunishCash;

    [XmlElement("Suspended")]
    public int Suspended;

    [XmlElement("Description")]
    public string Description;

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

    [XmlElement("Name")]
    public string Name;

    [XmlElement("TotalCash")]
    public int TotalCash;

    [XmlElement("Installment")]
    public bool Installment;

    [XmlElement("MonthToPay")]
    public int MonthToPay;

    [XmlElement("CashPerMonth")]
    public int CashPerMonth;

    [XmlElement("Description")]
    public string Description;

    [XmlElement("ConnectionPoint")]
    public int ConnectionPoint;

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

    [XmlElement("TotalCash")]
    public int TotalCash;

    [XmlElement("ConnectionPoint")]
    public int ConnectionPoint;

    [XmlElement("TotalTime")]
    public int TotalTime;

    [XmlElement("Description")]
    public string Description;

    [XmlElement("ContinuedTime")]
    public int ContinuedTime;

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

    [XmlElement("TotalCash")]
    public int TotalCash;

    [XmlElement("BookNeeds")]
    public int BookNeeds;

    [XmlElement("RelationshipPointNeeds")]
    public int RelationshipPointNeeds;

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

    [XmlElement("Name")]
    public string Name;

    [XmlElement("Post")]
    public string Post;

    [XmlElement("PersonRequire")]
    public int PersonRequire;

    [XmlElement("StartMonth")]
    public int StartMonth;

    [XmlElement("EndMonth")]
    public int EndMonth;

    private double hourlySalary = 160;
    [XmlElement("HourlySalary")]
    public double HourlySalary
    {
        get { return hourlySalary; }
        set { hourlySalary *= value; }
    }

    [XmlElement("WeeklyTime")]
    public int WeeklyTime;

    [XmlElement("MonthlySalary")]
    private int monthlySalary;
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

    [XmlElement("MonthlyTime")]
    public int MonthlyTime;

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

    [XmlElement("MonthlyRequire")]
    public int MonthlyRequire;

    [XmlElement("OtherRequire")]
    public bool OtherRequire;

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

    [XmlElement("Type")]
    public int Type;

    [XmlElement("Name")]
    public string Name;

    [XmlElement("BookNums")]
    public int BookNums;

    [XmlElement("TotalCash")]
    public string TotalCash;

    [XmlElement("PersonRequire")]
    public bool PersonRequire;

    [XmlElement("UseTime")]
    public bool UseTime;

    [XmlElement("WeeklyTime")]
    public int WeeklyTime;

    [XmlElement("MonthlyTime")]
    public int MonthlyTime;

    [XmlElement("ConnectionPoint")]
    public int ConnectionPoint;

    [XmlElement("Punish_ConnectionPoint")]
    public int Punish_ConnectionPoint;

    [XmlElement("MonthNeeds")]
    public int MonthNeeds;

    [XmlElement("Description")]
    public string Description;

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
    public bool Relationship;
    public string Birth = string.Empty;
    public int PocketMoney;
    public int LivingExpend;
    public int Expending = 0;
    public int ConnectionPoint = 30;
    public int Suspended = 0;
    public List<WorkList> workList = new List<WorkList>();
    public List<Staging> stagings = new List<Staging>();
    public int BookNum = 0;
    public int Salary;

    private int SetallocateCash()
    {
        return (PocketMoney + Salary) - LivingExpend - Expending;
    }
    public int AllocateCash
    {
        get { return SetallocateCash(); }
        set { }
    }

    public int AllocateTime = 200;

}


[System.Serializable]
public class WorkList
{
    public int ID;
    public string Name = string.Empty;
    public string Post = string.Empty;
    public bool OnWork = true;
    public int Time;
    public int Salary;
    public int MonthlyRequire;
}

[System.Serializable]
public class ActivityList
{

}

[System.Serializable]
public class Staging
{
    public bool TotheEndOfGame = false;
    public string Name = string.Empty;
    public int CashPerMonth = 0;
    public int LeftMonth = 0;
}

#endregion