using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Photon.Pun;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class ConnectToServer : MonoBehaviourPunCallbacks
{
    public GameObject LobbyPanel;
    public GameObject LoadingText;
    public GameObject ConnectPanel;

    public InputField createInput;
    public InputField joinInput;

    void Start()
    {

    }

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
        PhotonNetwork.CreateRoom(createInput.text);
    }

    public void JoinRoom()
    {
        if (joinInput.text != "")
            PhotonNetwork.JoinRoom(joinInput.text);

    }

    public override void OnJoinedRoom()
    {
        PhotonNetwork.LoadLevel("ChareaterSelectScene");
    }
}
