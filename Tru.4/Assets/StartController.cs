using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StartController : MonoBehaviour
{
    public GameObject CharacterImage;

    private void Start()
    {
        LeanTween.moveLocalY(CharacterImage, -555, 1f).setEase(LeanTweenType.pingPong).setLoopPingPong();
    }
}
