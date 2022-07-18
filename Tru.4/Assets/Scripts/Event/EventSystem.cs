using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EventSystem : MonoBehaviour
{
    //卡牌類型：黑暗卡，投資卡，工作卡，學習卡，大/小爽卡，好運卡
    enum EventType { DarkCard, InvestCard, WorkCard, LearningCard, GreatCard, LittleLuck }

    [SerializeField]
    [Header("卡牌種類")]
    private EventType eventType = new EventType();

    [HideInInspector]
    public EventManager eventManager;
    [HideInInspector]
    public bool IsLittle = true;
    public SpriteRenderer EventImage;
    private  Sprite eventImage;

    private void Start()
    {
        #region 初始刷新場景圖示
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
        #endregion
    }

    public void DoEvent()
    {
        switch (eventType)
        {
            case EventType.DarkCard:
                eventManager.DoDarkCardEvent();
                break;

            case EventType.InvestCard:
                eventManager.DoInvestEvent();
                break;

            case EventType.GreatCard:
                eventManager.DoGreatCardEvent();
                break;

            case EventType.LearningCard:
                eventManager.DoLearningCardEvent();
                break;

            case EventType.LittleLuck:
                eventManager.DoLittleLuckEvent();
                break;

            case EventType.WorkCard:
                eventManager.DoWorkCardEvent();
                break;
        }
    }
}
