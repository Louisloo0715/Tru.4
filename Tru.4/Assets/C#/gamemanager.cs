using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class gamemanager : MonoBehaviour
{
    public void OnStartGame(string ScneneName)
    {
        Application.LoadLevel(ScneneName);
    }

        public void BroadcastMessage(string UI2)
    {
        Application.LoadLevel(UI2);
    }

        public void Cancelincoke(string UI1)
    {
        Application.LoadLevel(UI1);
    }

        public void SendMessage(string UI4)
    {
        Application.LoadLevel(UI4);
    }
    
        public void StopCoroutine(string UI3)
    {
        Application.LoadLevel(UI3);
    }
}
