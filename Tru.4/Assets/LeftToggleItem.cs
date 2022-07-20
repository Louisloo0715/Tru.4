using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LeftToggleItem : MonoBehaviour
{
    public WorkList work;

    public Text postText;
    public Text MonthTimeText;
    public Text SalaryText;

    private void Start()
    {
        LeftWorkToggleManager.Instance.leftToggleItems.Add(this);
    }

    private void Update()
    {
        MonthTimeText.text = "每月工作時間：" + work.Time;
        SalaryText.text = "每月薪資：" + work.Salary;
        postText.text = work.Post;
    }
}
