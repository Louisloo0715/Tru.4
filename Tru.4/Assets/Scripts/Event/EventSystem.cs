using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum EventType { None, DarkCard, InvestCard, WorkCard, LearningCard, LargeGreat, LittleGreat, LittleLuck }

public class EventSystem : MonoBehaviour
{
    
    public EventType eventType = new EventType();
    public GameObject ShowEventRandomSelection;

    private void Restart()
    {
        switch (eventType)
        {
            case EventType.None:
                break;
            case EventType.DarkCard:
                break;
            case EventType.InvestCard:
                break;
            case EventType.LargeGreat:
                break;
            case EventType.LearningCard:
                break;
            case EventType.LittleGreat:
                break;
            case EventType.LittleLuck:
                break;
            case EventType.WorkCard:
                break;
        }
    }
}
