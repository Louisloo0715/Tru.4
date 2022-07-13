using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Photon.Pun;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using Photon.Realtime;

public class ConnectToServer : MonoBehaviourPunCallbacks
{
    public GameObject LobbyPanel;
    public GameObject LoadingText;
    public GameObject ConnectPanel;

    public InputField createInput;
    public InputField joinInput;

    public GameObject SelectCavan;
    public List<FriendItem> playerItemsList = new List<FriendItem>();
    public Transform PanelGrid;
    public FriendItem PrefabItem;


    public void Connect()
    {
        LeanTween.scale(LobbyPanel, Vector3.one, .5f).setEase(LeanTweenType.easeInExpo);
        PhotonNetwork.ConnectUsingSettings();
    }

    public override void OnConnectedToMaster()
    {
        PhotonNetwork.JoinLobby();
    }

    public override void OnJoinedLobby()
    {
        LoadingText.SetActive(false);
        ConnectPanel.SetActive(true);
    }

    public void CreateRoom()
    {
        if (createInput.text != "")
            PhotonNetwork.CreateRoom(createInput.text);
    }

    public void JoinRoom()
    {
        if (joinInput.text != "")
            PhotonNetwork.JoinRoom(joinInput.text);
    }

    public void ExitRoom()
    {
        OnLeftRoom();
    }

    public override void OnJoinedRoom()
    {
        //PhotonNetwork.LoadLevel("ChareaterSelectScene");
        SelectCavan.SetActive(true);
        UpdateFriendList();
    }


    public override void OnLeftRoom()
    {
        LobbyPanel.transform.localScale = Vector3.zero;
        LoadingText.SetActive(true);
        ConnectPanel.SetActive(false);
        SelectCavan.SetActive(false);
        joinInput.text = "";
        createInput.text = "";
        PhotonNetwork.LocalPlayer.CustomProperties.Clear();
        PhotonNetwork.Disconnect();
        UpdateFriendList();
    }

    public override void OnLeftLobby()
    {
        base.OnLeftLobby();
    }
    void UpdateFriendList()
    {
        foreach (FriendItem item in playerItemsList)
        {
            Destroy(item.gameObject);
        }
        playerItemsList.Clear();

        if (PhotonNetwork.CurrentRoom == null)
            return;

        foreach (KeyValuePair<int, Photon.Realtime.Player> player in PhotonNetwork.CurrentRoom.Players)
        {
            FriendItem newFriendItem = Instantiate(PrefabItem, PanelGrid);
            playerItemsList.Add(newFriendItem);
        }
    }

    public override void OnPlayerEnteredRoom(Player newPlayer)
    {
        UpdateFriendList();
    }

    public override void OnPlayerLeftRoom(Player otherPlayer)
    {
        UpdateFriendList();
    }
}
