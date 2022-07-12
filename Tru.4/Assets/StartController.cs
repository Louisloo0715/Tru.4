using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class StartController : MonoBehaviour
{
    public GameObject CharacterImage;

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

    public void showPanel(GameObject gameObject)
    {
        LeanTween.scale(gameObject, Vector3.one, .5f).setEase(LeanTweenType.easeInExpo);

    }
    public void closePanel(GameObject gameObject)
    {
        LeanTween.scale(gameObject, Vector3.zero, .5f).setEase(LeanTweenType.easeInExpo);
    }

}
