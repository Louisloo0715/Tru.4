using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Xml;

public class SavePlayerData : MonoBehaviour
{
    public DataControl dataControl = DataControl.Instance;
    public string PlayerName;
    public int ID = 201;

    #region �����l�Ƽƾ�

    private int CheckStartJob(int _ID)
    {
        Characters temp = GetCharacter(_ID);

        if (temp.ID != 0)
            return temp.StartJob;
        else
            return 0;
    }

    private void CreateXML(Characters character,Jobs job)
    {
        string localPath = UnityEngine.Application.persistentDataPath + "/Player.xml";
        XmlDocument xml = new XmlDocument();
        XmlDeclaration xmldecl = xml.CreateXmlDeclaration("1.0", "UTF-8", "");//�]�mxml���s�X�榡?UTF-8
        XmlElement root = xml.CreateElement("PlayerData");//�Ыخڸ`�I
        XmlElement info = xml.CreateElement("Info");//�Ыؤl�`�I
        info.SetAttribute("PlayerName", PlayerName);//�Ыؤl�`�I�ݩʦW�M�ݩʭ�
        info.SetAttribute("Name", character.Name);
        if (character.Relationship == 0)
            info.SetAttribute("Relationship", "�L");
        else
            info.SetAttribute("Relationship", "��");
        info.SetAttribute("Birth", character.Birth);
        
        root.AppendChild(info);//�N�l�`�I���ӳЫض��ǡA�K�[��xml

        XmlElement Income = xml.CreateElement("Jobs");//�Ыؤl�`�I


        xml.AppendChild(root);
        xml.Save(localPath);//�O�sxml����|��m
        Debug.Log("�Ы�XML���\�I");
    }
    #endregion

    #region ����^��
    public Characters GetCharacter(int id)
    {
        foreach (var character in dataControl.Characters_DataBase.Obj)
        {
            if (character.ID != id)
                continue;
            else
                return character;
        }

        return null;
    }

    public Jobs Getjob(int id)
    {
        foreach (var job in dataControl.Jobs_DataBase.Obj)
        {
            if (job.ID != id)
                continue;
            else
                return job;
        }

        return null;
    }

    #endregion

    //void CreateXML(Characters character)
    //{
    //    string localPath = UnityEngine.Application.persistentDataPath + "/Player.xml";

    //    XmlDocument xml = new XmlDocument();
    //    XmlDeclaration xmldecl = xml.CreateXmlDeclaration("1.0", "UTF-8", "");//�]�mxml���s�X�榡?UTF-8
    //    XmlElement root = xml.CreateElement("PlayerData");//�Ыخڸ`�I
    //    XmlElement info = xml.CreateElement("Info");//�Ыؤl�`�I
    //    info.SetAttribute("PlayerName", PlayerName);//�Ыؤl�`�I�ݩʦW�M�ݩʭ�
    //    info.SetAttribute("Name", character.Name);

    //    if (character.Relationship == 0)
    //        info.SetAttribute("Relationship", "�L");
    //    else
    //        info.SetAttribute("Relationship", "��");

    //    info.SetAttribute("Birth", character.Birth);
    //    root.AppendChild(info);//�N�l�`�I���ӳЫض��ǡA�K�[��xml
    //    xml.AppendChild(root);

    //    XmlElement Income = xml.CreateElement("Income");//�Ыؤl�`�I
    //    info.SetAttribute("PlayerName", PlayerName);
    //    xml.Save(localPath);//�O�sxml����|��m
    //    Debug.Log("�Ы�XML���\�I");
    //}
}
