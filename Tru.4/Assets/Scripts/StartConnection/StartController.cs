using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class StartController : MonoBehaviour
{
    public GameObject CharacterImage;
    public InputField inputName;

    private void Start()
    {
        LeanTween.moveLocalY(CharacterImage, -480, 1f).setEase(LeanTweenType.pingPong).setLoopPingPong();
    }
    
    public void LoadLevle(int sceneIndex)
    {
        StartCoroutine(LoadAsynchronously(sceneIndex));
    }

    IEnumerator LoadAsynchronously(int sceneIndex)
    {
        AsyncOperation operation = SceneManager.LoadSceneAsync(sceneIndex);

        while (!operation.isDone)
        {
            float progress = Mathf.Clamp01(operation.progress / .9f);
            Debug.Log(progress);
            yield return null;
        }
    }
    public void Exit()
    {
        Application.Quit();
    }

    public void PopUP(GameObject gameObject)
    {
        gameObject.SetActive(true);
        LeanTween.scale(gameObject, Vector3.one, .5f).setEase(LeanTweenType.easeInExpo);
    }

    public void CloseIt(GameObject gameObject)
    {
        LeanTween.scale(gameObject, Vector3.zero, .5f).setEase(LeanTweenType.easeInExpo);
        gameObject.SetActive(false);
    }

    public void CheckInput(GameObject gameObject)
    {
        if (inputName.text.Length > 4)
            PopUP(gameObject);
        else
        { 
            ConnectToServer.Instance.Name = inputName.text;
            ConnectToServer.Instance.Connect();
        }

    }
}
