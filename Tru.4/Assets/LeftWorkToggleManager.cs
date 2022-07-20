using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LeftWorkToggleManager : MonoBehaviour
{
    public List<LeftToggleItem> leftToggleItems = new List<LeftToggleItem>();
    public LeftToggleItem SelectToggle;
    public static LeftWorkToggleManager Instance;
    private void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(this);
    }

    public void ClearItem()
    {
        leftToggleItems.Clear();
    }
    
}
