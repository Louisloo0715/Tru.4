using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScratchCardEffect : MonoBehaviour
{
    public GameObject maskPrefab;
    private bool isPressed = false;

    private void Update()
    {
        var mousePos = Input.mousePosition;
        mousePos.z = 2;
        mousePos = Camera.main.ScreenToWorldPoint(mousePos);

        if (isPressed)
        {
            GameObject maskSprite = Instantiate(maskPrefab, mousePos, Quaternion.identity);
            maskSprite.transform.parent = gameObject.transform;
        }
        else
        {

        }
        if (Input.GetMouseButtonDown(0))
        {
            Invoke("reveal", 5);
            isPressed = true;
        }
        else if (Input.GetMouseButtonUp(0))
            isPressed = false;
    }

    void reveal()
    {
        Destroy(this.gameObject);
    }

}
