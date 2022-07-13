using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Photon.Pun;
using Photon.Realtime;

public class FriendItem : MonoBehaviour
{
    public Text playerName;
    public Image playerImage;

    ExitGames.Client.Photon.Hashtable playerProperties = new ExitGames.Client.Photon.Hashtable();
    public Image playerAvatar;
    public Dictionary<int, Sprite> avatars = new Dictionary<int, Sprite>();
    public void SetPlayerInfo(Player _player)
    {
        playerName.text = _player.NickName;
    }
  
    private void Update()
    {
        playerImage.sprite = Resources.Load<Sprite>("CharacterSelect/" + ConnectToServer.Instance.ID + "/HeadImage");
    }

    public void ApplyLocalChage()
    { 
    
    }

}
