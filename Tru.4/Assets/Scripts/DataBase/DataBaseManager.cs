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

    [XmlElement("Relationship")]
    public int Relationship;

    [XmlElement("PocketMoney")]
    public int PocketMoney;

    [XmlElement("Salary")]
    public int Salary;

    [XmlElement("LivingExpend")]
    public int LivingExpend;

    [XmlElement("StartJob")]
    public int StartJob;

    [XmlElement("AllocateCash")]
    public string AllocateCash;

    [XmlElement("AllocateTime")]
    public string AllocateTime;

}
#endregion

#region 工作資料
[XmlRoot("JobsExperience")]
public class JobsExperience
{
    [XmlArray("Jobs")]
    [XmlArrayItem("Job")]
    public List<Jobs> Obj = new List<Jobs>();

    public static JobsExperience LoadDataBase(string path)
    {
        TextAsset _xml = Resources.Load<TextAsset>(path);
        XmlSerializer serializer = new XmlSerializer(typeof(JobsExperience));
        StringReader reader = new StringReader(_xml.text);
        JobsExperience Obj = new JobsExperience();
        Obj = serializer.Deserialize(reader) as JobsExperience;
        reader.Close();
        return Obj;
    }
}

public class Jobs
{
    [XmlAttribute("Job")]
    public string InteractiveObj;

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

    //private int hourlySalary = 168;

    [XmlElement("HourlySalary")]
    public int HourlySalary;
    //{ 
    //    get { return hourlySalary * HourlySalary; }
    //    set { hourlySalary = value; }
    //}


    [XmlElement("MonthlySalary")]
    public int MonthlySalary;

    [XmlElement("AnnualSalary")]
    public int AnnualSalary;

    [XmlElement("WeeklyTime")]
    public int WeeklyTime;

    [XmlElement("MonthlyTime")]
    public int MonthlyTime;

    [XmlElement("MonthlyRequire")]
    public int MonthlyRequire;

    [XmlElement("OtherRequire")]
    public int OtherRequire;
}
#endregion


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
         Obj =  serializer.Deserialize(reader) as DarkCardsDataBase;
        reader.Close();
        return Obj;
    }
}

public class DarkCards
{
    [XmlAttribute("Card")]
    public string Card;

    [XmlElement("ID")]
    public int ID;

    [XmlElement("PunishTime")]
    public string PunishTime;

    [XmlElement("PunishCash")]
    public string PunishCash;

    [XmlElement("Suspended")]
    public int Suspended;

    [XmlElement("OtherRequire")]
    public int OtherRequire;
}
