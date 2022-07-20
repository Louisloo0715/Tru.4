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

    [Header("黑暗卡Panel")]
    public GameObject LeftWorkPanel;
    public GameObject LeftWorkTogglePrefab;
    public GameObject LeftWorkGrid;

    [Header("工作卡Panel")]
    public GameObject WorkPanel;

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

    #region 顯示內容敘述
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
    bool isPress()
    { return ispress; }
    public void Press(bool isPress)
    {
        ispress = isPress;
    }
    #endregion

    #region 執行黑暗卡事件
    public void DoDarkCardEvent(PlayerData playerData)
    {
        if (DarkCardNum == DataControl.Instance.DarkCards_DataBase.Count)
            return;
        DarkCardNum++;
        DarkCards card = dataControl.DarkCards_DataBase[DarkCardNum];
        StartCoroutine(Decripction(card.Description));

        if (!card.OtherRequire)
            DoNormalDark(playerData, card);
        else
        {
            switch (card.ID)
            {
                case 4://離開當前其中一份工作
                    StartCoroutine(LeftOneJob(playerData));
                    break;

                case 5://打工超過100小時
                    int sum = 0;
                    foreach (var work in playerData._playerData.workList)
                    {
                        sum += work.Time;
                    }
                    if (sum > 100)
                        DoNormalDark(playerData, card);
                    break;

                case 7://離開當前其中一份工作
                    StartCoroutine(LeftOneJob(playerData));
                    break;

                case 12://離開當前薪水最高的一份工作
                    LeftHightestWork(playerData);
                    break;

                case 13://離開當前其中一份工作
                    StartCoroutine(LeftOneJob(playerData));
                    break;
            }
        }
        Dice.Instance.coroutineAllowed = true;
    }

    private void DoNormalDark(PlayerData player, DarkCards card)
    {
        player._playerData.Expending += card.PunishCash;
        player._playerData.AllocateTime -= card.PunishTime;
        player._playerData.Suspended = card.Suspended;
    }//一般數值加減
    private IEnumerator LeftOneJob(PlayerData player)
    {
        if (player._playerData.workList.Count == 0)//玩家若無工作則跳過
            StopCoroutine(LeftOneJob(player));

        if (player._playerData.workList.Count == 1 && player._playerData.workList[0].MonthlyRequire == -1)//玩家自帶工作不可辭職
            StopCoroutine(LeftOneJob(player));

        if (LeftWorkGrid.transform.childCount != 0)
        {
            for (int i = 0; i < LeftWorkGrid.transform.childCount; i++)
            {
                Destroy(LeftWorkGrid.transform.GetChild(i).gameObject);
            }
        }//清空玩家工作列表UI

        LeanTween.scale(LeftWorkPanel, Vector3.one, .5f).setEase(LeanTweenType.easeInExpo);
        foreach (var work in player._playerData.workList)
        {
            if (work.MonthlyRequire == -1)//列表不可出現玩家自帶工作
                continue;
            if (!work.OnWork)
                continue;

            GameObject _work = Instantiate(LeftWorkTogglePrefab, LeftWorkGrid.transform.position, Quaternion.identity);
            _work.GetComponent<LeftToggleItem>().work = work;

            _work.GetComponent<Toggle>().group = LeftWorkGrid.GetComponent<ToggleGroup>();

            _work.transform.SetParent(LeftWorkGrid.transform);
            _work.transform.localScale = Vector3.one;
        }//生成玩家工作列表UI

        yield return new WaitUntil(lwSubmit);//暫停此方法直到玩家按下按鈕確認
        LWSubmit = false;
        foreach (var toggle in LeftWorkToggleManager.Instance.leftToggleItems)
        {
            if (!toggle.GetComponent<Toggle>().isOn)
                continue;
            LeftWorkToggleManager.Instance.SelectToggle = toggle;
        }//找出玩家選擇的工作

        foreach (var work in player._playerData.workList)
        {
            if (LeftWorkToggleManager.Instance.SelectToggle.work.ID != work.ID)
                continue;
            else
                work.OnWork = false;
        }//移除玩家工作工作中變為False

        LeftWorkToggleManager.Instance.ClearItem();

    }//玩家選擇離開當前其中一份工作
    private void LeftHightestWork(PlayerData player)
    {
        WorkList _work = new WorkList();
        if (player._playerData.workList.Count == 0)
            return;
        if (player._playerData.workList.Count == 1 && player._playerData.workList[0].MonthlyRequire == -1)
            return;

        foreach (var work in player._playerData.workList)
        {
            if (work.MonthlyRequire == -1)
                continue;

            if (work.Salary > _work.Salary)
                _work = work;
            else
                continue;
        }
        player._playerData.workList.Find(x => x.ID == _work.ID).OnWork = false;

    }//離開薪水最高的工作

    private bool LWSubmit = false;
    bool lwSubmit()
    { return LWSubmit; }
    public void LeftWorkSubmit()
    {
        if (LeftWorkGrid.GetComponent<ToggleGroup>().AnyTogglesOn())
            LWSubmit = true;
        else
            LWSubmit = false;
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

                    case 34:
                        if (!playerData._playerData.Relationship)
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
    public IEnumerator DoWorkCardEvent(PlayerData playerData)
    {
        if (WorkCardNum == DataControl.Instance.Work_DataBase.Count)
            StopCoroutine(DoWorkCardEvent(playerData));
        WorkCardNum++;
        Works card = DataControl.Instance.Work_DataBase[WorkCardNum];

        if (!card.OtherRequire)//詢問是否要應徵此工作
        {
            yield return new WaitUntil(isPress);
            ispress = false;
            if (isWant)
            { playerData._playerData.workList.Add(AddNormalWork(card)); }
            else 
            { yield return null; }
               
        }
        else
        {
            switch (WorkCardNum)
            {
                case 7:
                    break;

                case 8:
                    break;

                case 10:
                    break;

                case 11:
                    break;

                case 12:
                    break;

                case 13:
                    break;

                case 15:
                    break;

                case 17:
                    break;

                case 18:
                    break;

                case 19:
                    break;

                case 20:
                    break;

                case 21:
                    break;

                case 22:
                    break;

                case 23:
                    break;

                case 24:
                    break;

                case 25:
                    break;
            }
        }

        yield return null;
    }

    private bool isWant = false;
    public void IsWantThisWork(bool iswant)
    { isWant = iswant; }

    private WorkList AddNormalWork(Works card)
    {
        WorkList work = new WorkList();
        work.ID = card.ID;
        work.Name = card.Name;
        work.Post = card.Post;
        work.Time = card.MonthlyTime;
        work.Salary = card.MonthlySalary;
        work.MonthlyRequire = card.MonthlyRequire;

        return work;
    }//返回當前工作資訊

    #endregion


}
