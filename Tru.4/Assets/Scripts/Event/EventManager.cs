using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EventManager : MonoBehaviour
{
    public int DarkCardNum = 0;
    public int WorkCardNum = 0;
    public int LearningCard = 0;
    public int LittleLuck = 0;
    public int InvestCard = 0;

    public List<EventSystem> events = new List<EventSystem>();

    public void Start()
    {
        foreach (var _event in events)
        {
            _event.eventManager = this;
        }
    }
}
