using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class EventManager : MonoBehaviour
{
    public int DarkCardNum = 0;
    public int WorkCardNum = 0;
    public int LearningCard = 0;
    public int LittleLuck = 0;
    public int InvestCard = 0;

    public List<EventSystem> events = new List<EventSystem>();
    private DataControl dataControl;

    public void Start()
    {
        foreach (var _event in events)
        {
            _event.eventManager = this;
        }
        dataControl = DataControl.Instance;
    }

    public void DoDarkCardEvent()
    {
        if (DarkCardNum == DataControl.Instance.DarkCards_DataBase.Count)
            return;
        DarkCardNum++;
        dataControl._playerData.AllocateCash -= dataControl.DarkCards_DataBase[DarkCardNum].PunishCash;
        dataControl._playerData.AllocateTime -= dataControl.DarkCards_DataBase[DarkCardNum].PunishTime;
        dataControl._playerData.Suspended = dataControl.DarkCards_DataBase[DarkCardNum].Suspended;
    }

    public void DoInvestEvent()
    {

    }

    public void DoGreatCardEvent()
    {
        if (DataControl.Instance._playerData.AllocateCash >= 6000)
        {
            int ran = Random.Range(0, dataControl.LargeGreats_DataBase.Count);
            LargeGreatCard card = dataControl.LargeGreats_DataBase[ran];
        }
        else
        {
            int ran = Random.Range(0, dataControl.LittleGreats_DataBase.Count);
            LittleGreatCard card = dataControl.LittleGreats_DataBase[ran];
        }

    }

    public void DoLearningCardEvent()
    {
    }

    public void DoLittleLuckEvent()
    {
        if (LittleLuck == DataControl.Instance.LittleLuck_DataBase.Count)
            return;
        LittleLuck++;
    }

    public void DoWorkCardEvent()
    {
        if (WorkCardNum == DataControl.Instance.Work_DataBase.Count)
            return;
        WorkCardNum++;
    }
}
