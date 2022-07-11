using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CharacterSelectItem : MonoBehaviour
{
    public int ID = 0;
    public CharacterSelectControl selectControl;
    public Image HeadImage;

    private void Update()
    {
        if (ID != 0)
        {
            string path = "CharacterSelect/" + ID + "/HeadImage";
            HeadImage.sprite = Resources.Load<Sprite>(path);

        }
        else
            return;
    }

    public void GetHit()
    {
        selectControl.setupInfo(ID);
    }
}
