using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//刮刮樂做法拿取卡片
public class ScratchCardEffect : MonoBehaviour
{
    public GameObject maskPrefab;
    public Camera _camera;
    private bool isPressed = false;

    private void Update()
    {
        var mousePos = Input.mousePosition;
        mousePos.z = 2;
        mousePos = _camera.ScreenToWorldPoint(mousePos);

        if (isPressed)
        {
            GameObject maskSprite = Instantiate(maskPrefab, mousePos, Quaternion.identity);
            maskSprite.transform.parent = gameObject.transform;
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
