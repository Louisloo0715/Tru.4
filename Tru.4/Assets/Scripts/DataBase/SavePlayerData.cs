using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Xml;

public class SavePlayerData : MonoBehaviour
{
    public DataControl dataControl = DataControl.Instance;
    public string PlayerName;

    #region 角色初始化數據

    private int CheckStartJob(int _ID)
    {
        Characters temp = dataControl.Characters_DataBase[_ID];

        if (temp.ID != 0)
            return temp.StartJob;
        else
            return 0;
    }

    private void CreateXML(Characters character)
    {
        string localPath = UnityEngine.Application.persistentDataPath + "/Player.xml";
        XmlDocument xml = new XmlDocument();
        XmlDeclaration xmldecl = xml.CreateXmlDeclaration("1.0", "UTF-8", "");//設置xml文件編碼格式?UTF-8
        XmlElement root = xml.CreateElement("PlayerData");//創建根節點
        XmlElement info = xml.CreateElement("Info");//創建子節點
        info.SetAttribute("PlayerName", PlayerName);//創建子節點屬性名和屬性值
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
}
