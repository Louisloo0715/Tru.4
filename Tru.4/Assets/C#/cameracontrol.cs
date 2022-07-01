using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cameracontrol : MonoBehaviour
{
     public GameObject Newcamera;
    public GameObject Oldcamera;

    private void OnTriggerStay(Collider other)
    {
        SwitchCamera();
    }
    public void SwitchCamera()
    {
        Newcamera.GetComponent<Camera>().enabled = true;
        Oldcamera.GetComponent<Camera>().enabled = false;
    }
      void Awake ()
    {

        Oldcamera.SetActive(false);
        Newcamera.SetActive(true);

    }
}