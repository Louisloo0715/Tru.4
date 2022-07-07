using System.Collections.Generic;
using System.Xml;
using System.Xml.Linq;
using UnityEngine;
using System.Runtime.Serialization.Formatters.Binary;
using System.IO;

public class SavePlayerData : MonoBehaviour
{
    public DataControl dataControl =new DataControl();
    public PlayerDataBase dataBase = new PlayerDataBase();
    public string PlayerName;

    #region 角色初始化數據

    private void Start()
    {
        dataControl = DataControl.Instance;
    }

    private int CheckStartJob(int _ID)
    {
        Characters temp = dataControl.Characters_DataBase[_ID];

        if (temp.ID != 0)
            return temp.StartJob;
        else
            return 0;
    }

    private void CreateXML(Characters character, int id)
    {
        string localPath = UnityEngine.Application.persistentDataPath + "/Player.xml";
        XmlDocument xml = new XmlDocument();
        XmlDeclaration xmldecl = xml.CreateXmlDeclaration("1.0", "UTF-8", "");//設置xml文件編碼格式?UTF-8
        XmlElement root = xml.CreateElement("PlayerData");//創建根節點

        XmlElement info = xml.CreateElement("Info");//創建子節點
        info.SetAttribute("PlayerName", PlayerName);//創建子節點屬性名和屬性值
        foreach (var player in DataControl.Instance.Characters_DataBase)
            info.SetAttribute("Name", character.Name);
        info.SetAttribute("Relationship", character.Relationship);
        info.SetAttribute("Birth", character.Birth);

        root.AppendChild(info);//將子節點按照創建順序，添加到xml

        XmlElement Income = xml.CreateElement("Jobs");//創建子節點


        xml.AppendChild(root);
        xml.Save(localPath);//保存xml到路徑位置
        Debug.Log("創建XML成功！");
    }
    #endregion



    #region 資料擷取


    //public Jobs Getjob(int id)
    //{
    //    foreach (var job in dataControl.Jobs_DataBase.Obj)
    //    {
    //        if (job.ID != id)
    //            continue;
    //        else
    //            return job;
    //    }

    //    return null;
    //}

    #endregion

    //void CreateXML(Characters character)
    //{
    //    string localPath = UnityEngine.Application.persistentDataPath + "/Player.xml";

    //    XmlDocument xml = new XmlDocument();
    //    XmlDeclaration xmldecl = xml.CreateXmlDeclaration("1.0", "UTF-8", "");//設置xml文件編碼格式?UTF-8
    //    XmlElement root = xml.CreateElement("PlayerData");//創建根節點
    //    XmlElement info = xml.CreateElement("Info");//創建子節點
    //    info.SetAttribute("PlayerName", PlayerName);//創建子節點屬性名和屬性值
    //    info.SetAttribute("Name", character.Name);

    //    if (character.Relationship == 0)
    //        info.SetAttribute("Relationship", "無");
    //    else
    //        info.SetAttribute("Relationship", "有");

    //    info.SetAttribute("Birth", character.Birth);
    //    root.AppendChild(info);//將子節點按照創建順序，添加到xml
    //    xml.AppendChild(root);

    //    XmlElement Income = xml.CreateElement("Income");//創建子節點
    //    info.SetAttribute("PlayerName", PlayerName);
    //    xml.Save(localPath);//保存xml到路徑位置
    //    Debug.Log("創建XML成功！");
    //}

    public void SavingOri()
    {
        Save(CreatOriDataBase());
    }

    public void Saving(PlayerDataBase playerData)
    {
        BinaryFormatter formatter = new BinaryFormatter();
        string Path = UnityEngine.Application.persistentDataPath + "/Player.txt";

        FileStream stream = new FileStream(Path, FileMode.Create);
        PlayerDataBase dataBase = new PlayerDataBase();

        formatter.Serialize(stream, dataBase);
        stream.Close();
    }

    private PlayerDataBase CreatOriDataBase()
    {
        PlayerDataBase dataBase = new PlayerDataBase();
        dataBase.PlayerName = PlayerName;
        Characters character = dataControl.Characters_DataBase[dataControl.ID];
        dataBase.Name = character.Name;
        dataBase.Birth = character.Birth;
        dataBase.LivingExpend = character.LivingExpend;
        dataBase.PocketMoney = character.PocketMoney;
        dataBase.Relationship = character.Relationship;
        return dataBase;
    }

    public static void Save(PlayerDataBase allData)
    {
        string saveString = JsonUtility.ToJson(allData, true);
        var filePath = Application.persistentDataPath;
        StreamWriter file = new StreamWriter(System.IO.Path.Combine(filePath, "Player.json"));
        file.Write(saveString);
        file.Close();
    }

    /*public static AllData LoadAllData(string filename)
    {
        var filePath = Application.persistentDataPath;
        StreamReader fileReader = new StreamReader(System.IO.Path.Combine(filePath, filename));
        string stringJson = fileReader.ReadToEnd();
        fileReader.Close();
        AllData num = JsonUtility.FromJson<AllData>(stringJson);
        return num;
    }*/
}
