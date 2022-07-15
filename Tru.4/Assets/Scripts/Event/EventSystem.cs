using System.Collections;
using System.Collections.Generic;
using UnityEngine;




public class EventSystem : MonoBehaviour
{
    enum EventType { DarkCard, InvestCard, WorkCard, LearningCard, GreatCard, LittleLuck }

    [SerializeField]
    private EventType eventType = new EventType();
    public GameObject ShowEventRandomSelection;

    public EventManager eventManager;
    public bool IsLittle = true;
    public SpriteRenderer EventImage;
    private  Sprite eventImage;

    private void Start()
    {
        switch (eventType)
        {
            case EventType.DarkCard:
                eventImage = Resources.Load<Sprite>("EventImage/黑暗");
                break;
            case EventType.GreatCard:
                eventImage = Resources.Load<Sprite>("EventImage/小爽");
                break;
            case EventType.InvestCard:
                eventImage = Resources.Load<Sprite>("EventImage/投資");
                break;
            case EventType.LearningCard:
                eventImage = Resources.Load<Sprite>("EventImage/學習");
                break;
            case EventType.LittleLuck:
                eventImage = Resources.Load<Sprite>("EventImage/好運");
                break;
            case EventType.WorkCard:
                eventImage = Resources.Load<Sprite>("EventImage/工作");
                break;
        }

        EventImage.sprite = eventImage;
    }

    public void Restart()
    {
        switch (eventType)
        {
            case EventType.DarkCard:
                if (DataControl.Instance.DarkCards_DataBase.Count == eventManager.DarkCardNum)
                    return;
                eventManager.DarkCardNum++;
                Debug.Log("DarkCardNum：" + eventManager.DarkCardNum);
                break;
            case EventType.InvestCard:
                eventManager.InvestCard++;
                Debug.Log("InvestCard：" + eventManager.InvestCard);
                break;
            case EventType.GreatCard:

                if (IsLittle)
                {
                    int ran = Random.Range(1, DataControl.Instance.LittleGreats_DataBase.Count);
                    Debug.Log("LittleGreat：" + ran);
                }
                else
                {
                    int ran = Random.Range(1, DataControl.Instance.LargeGreats_DataBase.Count);
                    Debug.Log("LargeGreat：" + ran);
                }

                break;
            case EventType.LearningCard:
                eventManager.LearningCard++;
                Debug.Log("LearningCard：" + eventManager.LearningCard);
                break;
            case EventType.LittleLuck:
                if (DataControl.Instance.LittleLuck_DataBase.Count == eventManager.LittleLuck)
                    return;
                eventManager.LittleLuck++;
                Debug.Log("LittleLuck：" + eventManager.LittleLuck);
                break;
            case EventType.WorkCard:
                if (DataControl.Instance.Work_DataBase.Count == eventManager.WorkCardNum)
                    return;
                eventManager.WorkCardNum++;
                Debug.Log("Work_DataBase：" + eventManager.WorkCardNum);
                break;
        }
    }
}
