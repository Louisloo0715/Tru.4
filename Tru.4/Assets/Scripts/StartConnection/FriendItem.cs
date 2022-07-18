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

    private PhotonView pvCache = null;
    public PhotonView photonView
    {
        get
        {
            if (pvCache == null)
                pvCache = PhotonView.Get(this);
            return pvCache;
        }
    }

    ExitGames.Client.Photon.Hashtable playerProperties = new ExitGames.Client.Photon.Hashtable();
    public Dictionary<int, Sprite> avatars = new Dictionary<int, Sprite>();

    public void SetPlayerInfo(Player _player)
    {
        playerName.text = _player.NickName;
    }

    private void Update()
    {
        if (photonView.IsMine)
            playerImage.sprite = Resources.Load<Sprite>("CharacterSelect/" + ConnectToServer.Instance.ID + "/HeadImage");
    }

    public void ApplyLocalChange()
    { 
    
    }
}
