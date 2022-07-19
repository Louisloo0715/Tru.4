using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
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

    [Header("敘述Panel")]
    public GameObject DescriptPanel;
    public Text DescriptText;

    [Header("大爽卡Panel")]
    public GameObject StagingPanel;

    public static EventManager Instance;
    private void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(this);
    }

    public void Start()
    {
        foreach (var _event in events)
        {
            _event.eventManager = this;
        }
        dataControl = DataControl.Instance;
    }

    #region 執行黑暗卡事件
    public void DoDarkCardEvent(PlayerData playerData)
    {
        if (DarkCardNum == DataControl.Instance.DarkCards_DataBase.Count)
            return;
        DarkCardNum++;

        playerData._playerData.Expending += dataControl.DarkCards_DataBase[DarkCardNum].PunishCash;
        playerData._playerData.AllocateTime -= dataControl.DarkCards_DataBase[DarkCardNum].PunishTime;
        playerData._playerData.Suspended = dataControl.DarkCards_DataBase[DarkCardNum].Suspended;

        Dice.Instance.coroutineAllowed = true;
    }
    #endregion

    #region 執行投資卡事件
    public void DoInvestEvent()
    {

    }
    #endregion

    #region 執行大/小爽卡事件

    private bool ischose = false;
    private bool isStaging = false;
    public IEnumerator DoGreatCardEvent(PlayerData playerData)
    {
        if (playerData._playerData.AllocateCash >= 6000)//大爽卡
        {
            int ran = Random.Range(1, dataControl.LargeGreats_DataBase.Count);
            LargeGreatCard card = dataControl.LargeGreats_DataBase[ran];
            StartCoroutine(Decripction(card.Description));
            if (card.Installment)//是否可分期
            {
                LeanTween.scale(StagingPanel, Vector3.one, .5f).setEase(LeanTweenType.easeInExpo);
                yield return new WaitUntil(IsChose);

                if (isStaging)
                    CheckWillStaging(playerData, card);
                else
                {
                    playerData._playerData.Expending += card.TotalCash;//扣除所有費用
                    playerData._playerData.ConnectionPoint += card.ConnectionPoint;//人脈點數的增加
                }
            }
            else
            {
                if (!card.OtherRequire)
                {
                    playerData._playerData.Expending += card.TotalCash;
                    playerData._playerData.ConnectionPoint += card.ConnectionPoint;
                }
                else
                {
                    switch (ran)//擁有其餘條件之選項
                    {
                        case 11:
                            playerData._playerData.Expending = playerData._playerData.AllocateCash;//條件當月可支配所得歸零
                            playerData._playerData.ConnectionPoint += card.ConnectionPoint;
                            break;

                        case 16:
                            Staging staging = new Staging();
                            staging.TotheEndOfGame = true;
                            staging.Name = card.Name; //名稱
                            staging.CashPerMonth = card.CashPerMonth;

                            playerData._playerData.Expending += card.CashPerMonth;
                            playerData._playerData.ConnectionPoint += card.ConnectionPoint;
                            playerData._playerData.stagings.Add(staging);
                            break;
                    }
                }
            }
        }
        else
        {
            int ran = Random.Range(1, dataControl.LittleGreats_DataBase.Count);
            LittleGreatCard card = dataControl.LittleGreats_DataBase[ran];
            StartCoroutine(Decripction(card.Description));
            if (!card.OtherRequire)
            {
                LittleGreatevent(playerData, card);
            }
            else
            {
                switch (card.ID)
                {
                    case 8:
                        LittleGreatevent(playerData, card);
                        //每位玩家都可以選擇是否參加
                        break;

                    case 21:
                        if (!playerData._playerData.Relationship)
                            break;
                        LittleGreatevent(playerData, card);
                        break;

                    case 33:
                        LittleGreatevent(playerData, card);
                        //自由樂捐
                        break;

                    case 34:if (!playerData._playerData.Relationship)
                            break;
                        LittleGreatevent(playerData, card);
                        break;

                }
            }
        }

        Debug.Log(playerData._playerData.AllocateCash);
        ischose = false;
        Dice.Instance.coroutineAllowed = true;
    }
    public void Chose(bool chose = true)
    { ischose = chose; }
    bool IsChose()
    {
        return ischose;
    }
    public void Staging(bool isstaging)
    {
        isStaging = isstaging;
    }
    private void CheckWillStaging(PlayerData player, LargeGreatCard card)//建立每月分期，且扣除當月
    {
        Staging staging = new Staging();

        staging.Name = card.Name; //名稱
        staging.CashPerMonth = card.CashPerMonth; //每月需支付費用
        staging.LeftMonth = card.MonthToPay;//還需支付的月數

        player._playerData.Expending += card.CashPerMonth;//先扣除第一期費用
        player._playerData.ConnectionPoint += card.ConnectionPoint;//人脈點數的增加

        staging.LeftMonth--;
        player._playerData.stagings.Add(staging);
    }

    private void LittleGreatevent(PlayerData player, LittleGreatCard card)
    {
        player._playerData.Expending += card.TotalCash;
        player._playerData.ConnectionPoint += card.ConnectionPoint;
        player._playerData.AllocateTime -= card.TotalTime;
    }
    #endregion

    #region 執行學習卡事件
    public void DoLearningCardEvent()
    {
    }
    #endregion

    #region 執行好運卡事件
    public void DoLittleLuckEvent()
    {
        if (LittleLuck == DataControl.Instance.LittleLuck_DataBase.Count)
            return;
        LittleLuck++;
    }
    #endregion

    #region 執行工作卡事件
    public void DoWorkCardEvent()
    {
        if (WorkCardNum == DataControl.Instance.Work_DataBase.Count)
            return;
        WorkCardNum++;
    }
    #endregion

    public void CloseIt(GameObject gameObject)
    {
        LeanTween.scale(gameObject, Vector3.zero, .5f).setEase(LeanTweenType.easeInExpo);
    }

    public IEnumerator Decripction(string Text)
    {
        LeanTween.scale(DescriptPanel, Vector3.one, .5f).setEase(LeanTweenType.easeInExpo);
        DescriptText.text = Text;
        yield return new WaitUntil(isPress);
        ispress = false;
    }

    private bool ispress = false;
    public void Press(bool isPress)
    {
        ispress = isPress;
    }

    bool isPress()
    { return ispress; }
}
