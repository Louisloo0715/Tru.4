using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
public class gamecontroller : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void QuitGame()
    {
        Application.Quit();
    }

    public void switchScene1() 
    {
        SceneManager.LoadScene(1);
    }

        public void switchScene2() 
    {
        SceneManager.LoadScene(2);
    }

        public void switchScene3() 
    {
        SceneManager.LoadScene(3);
    }

        public void switchScene4() 
    {
        SceneManager.LoadScene(4);
    }

        public void switchScene5() 
    {
        SceneManager.LoadScene(5);
    }

        public void switchScene6() 
    {
        SceneManager.LoadScene(6);
    }

        public void switchScene7() 
    {
        SceneManager.LoadScene(7);
    }

    public void switchScene0() 
    {
        SceneManager.LoadScene(0);
    }
}
