using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Xml.Serialization;
using System.IO;


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
            CharactersDataBase Obj = serializer.Deserialize(reader) as CharactersDataBase;
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
        public string Relationship;
        
        [XmlElement("PocketMoney")]
        public string PocketMoney;
        
        [XmlElement("Salary")]
        public string Salary;
        
        [XmlElement("LivingExpend")]
        public string LivingExpend;
        
        [XmlElement("StartJob")]
        public string StartJob;

        [XmlElement("AllocateCash")]
        public string AllocateCash;

        [XmlElement("AllocateTime")]
        public string AllocateTime;

    }
