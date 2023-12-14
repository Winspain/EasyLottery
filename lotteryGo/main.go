package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"github.com/robfig/cron/v3"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

var (
	lastRunResult int
	resultMutex   sync.Mutex
)

var prizeMap = map[string][]int{
	"first_prize":    {5, 2},
	"second_prize":   {5, 1},
	"third_prize":    {5, 0},
	"fourth_prize":   {4, 2},
	"fifth_prize":    {4, 1},
	"sixth_prize":    {3, 2},
	"seventh_prize":  {4, 0},
	"eighth_prize_1": {3, 1},
	"eighth_prize_2": {2, 2},
	"ninth_prize_1":  {3, 0},
	"ninth_prize_2":  {1, 2},
	"ninth_prize_3":  {2, 1},
	"ninth_prize_4":  {0, 2},
}

var prizeTransMap = map[string]string{
	"first_prize":    "一等奖",
	"second_prize":   "二等奖",
	"third_prize":    "三等奖",
	"fourth_prize":   "四等奖",
	"fifth_prize":    "五等奖",
	"sixth_prize":    "六等奖",
	"seventh_prize":  "七等奖",
	"eighth_prize_1": "八等奖",
	"eighth_prize_2": "八等奖",
	"ninth_prize_1":  "九等奖",
	"ninth_prize_2":  "九等奖",
	"ninth_prize_3":  "九等奖",
	"ninth_prize_4":  "九等奖",
}

func readConfig() [][]string {
	// 读取config.ini文件
	file, err := os.Open("config.ini")
	if err != nil {
		fmt.Println("无法打开文件:", err)
		return nil
	}
	defer file.Close()

	// 存储每组数字的切片
	var numberArrays [][]string

	// 逐行读取文件内容
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// 切分每行中的数字
		numbers := strings.Split(line, ",")
		// 将每组数字存入切片
		numberArrays = append(numberArrays, numbers)
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("读取文件时发生错误:", err)
		return nil
	}
	return numberArrays
}

func getPrizeResult(hitMap []int, prizeDict map[string][]int, prizeTransDict map[string]string) string {
	for prize, requirement := range prizeDict {
		if isEqual(hitMap, requirement) {
			return prizeTransDict[prize]
		}
	}
	return "未中奖"
}

func isEqual(arr1, arr2 []int) bool {
	if len(arr1) != len(arr2) {
		return false
	}

	for i := range arr1 {
		if arr1[i] != arr2[i] {
			return false
		}
	}

	return true
}

func getLatestNumberBy500() (map[string]string, error) {
	url := "http://datachart.500.com/dlt/history/history.shtml"

	response, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()

	if response.StatusCode != 200 {
		return nil, fmt.Errorf("HTTP request failed with status code: %d", response.StatusCode)
	}

	doc, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		return nil, err
	}

	lotteryTd := doc.Find("#tdata tr:first-child td")

	return map[string]string{
		"drawPeriod": lotteryTd.Eq(0).Text(),
		"frontNum1":  lotteryTd.Eq(1).Text(),
		"frontNum2":  lotteryTd.Eq(2).Text(),
		"frontNum3":  lotteryTd.Eq(3).Text(),
		"frontNum4":  lotteryTd.Eq(4).Text(),
		"frontNum5":  lotteryTd.Eq(5).Text(),
		"backNum1":   lotteryTd.Eq(6).Text(),
		"backNum2":   lotteryTd.Eq(7).Text(),
		"drawTime":   lotteryTd.Eq(14).Text(),
	}, nil
}

func getHitPrize(userSelect []string, latestNumber map[string]string) string {
	front := userSelect[:5]
	back := userSelect[5:]
	frontMap := make(map[string]string)
	backMap := make(map[string]string)
	frontHitCount := 0
	backHitCount := 0

	// 遍历原始map，检查键是否包含 "frontNum"，如果是则添加到新map
	for key, value := range latestNumber {
		if strings.Contains(key, "frontNum") {
			frontMap[key] = value
		}
		if strings.Contains(key, "backNum") {
			backMap[key] = value
		}
	}

	// 处理front
	//fmt.Println("与front匹配的数字和对应的字符串：")
	for _, frontNum := range front {
		for _, latestFrontNum := range frontMap {
			if strings.Contains(latestFrontNum, frontNum) {
				//fmt.Printf("%s: %s\n", key, latestFrontNum)
				frontHitCount += 1
			}
		}
	}

	// 处理back
	//fmt.Println("\n与back匹配的数字和对应的字符串：")
	for _, backNum := range back {
		for _, latestBackNum := range backMap {
			if strings.Contains(latestBackNum, backNum) {
				//fmt.Printf("%s: %s\n", key, latestBackNum)
				backHitCount += 1
			}
		}
	}
	hitMap := []int{frontHitCount, backHitCount}
	hitPrize := getPrizeResult(hitMap, prizeMap, prizeTransMap)
	return hitPrize
}

func sendDingDingNotification(hookUrl string, drawPeriod, drawTime string, hitPrizeArray []string, drawNum, userSelectString string) error {
	headers := map[string]string{
		"Content-Type": "application/json",
	}

	pushText := fmt.Sprintf("## 开奖期号:%s\n ## 开奖时间:%s\n ## 开奖结果:%v\n #### 开奖号码:\n%s\n#### 自选号码:\n%s", drawPeriod, drawTime, hitPrizeArray, drawNum, userSelectString)

	payload := map[string]interface{}{
		"msgtype": "markdown",
		"markdown": map[string]string{
			"title": drawPeriod,
			"text":  pushText,
		},
	}

	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("JSON marshaling failed: %v", err)
	}

	// Send POST request to the webhook URL with headers
	client := &http.Client{}
	req, err := http.NewRequest("POST", hookUrl, bytes.NewBuffer(jsonPayload))
	if err != nil {
		return fmt.Errorf("creating HTTP request failed: %v", err)
	}

	for key, value := range headers {
		req.Header.Set(key, value)
	}

	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("HTTP request failed: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	fmt.Println("DingDing notification sent successfully!")
	return nil
}

func run() {
	latestNum, err := getLatestNumberBy500()
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	drawPeriod := latestNum["drawPeriod"]
	drawTime := latestNum["drawTime"]
	drawNum := fmt.Sprintf(
		"[%s, %s, %s, %s, %s, %s, %s]",
		latestNum["frontNum1"],
		latestNum["frontNum2"],
		latestNum["frontNum3"],
		latestNum["frontNum4"],
		latestNum["frontNum5"],
		latestNum["backNum1"],
		latestNum["backNum2"],
	)

	result, err := strconv.Atoi(drawPeriod)
	if err != nil {
		fmt.Println("转换为整数失败：", err)
		return
	}

	// 对比返回值和全局变量
	resultMutex.Lock()
	defer resultMutex.Unlock()

	if result <= lastRunResult {
		// 如果返回值和全局变量+1相等，则不再运行
		currentTime := time.Now()
		fmt.Println("已通知，不再重复:", currentTime.Format("2006-01-02 15:04:05"))
		return
	}

	// 更新全局变量并继续运行
	lastRunResult = result
	fmt.Println("更新全局变量为：", lastRunResult)

	numberArrays := readConfig()
	hookUrl := numberArrays[0][0]

	var hitPrizeArray []string
	var userSelectString string
	for _, userSelect := range numberArrays[1:] {
		hitPrize := getHitPrize(userSelect, latestNum)
		hitPrizeArray = append(hitPrizeArray, hitPrize)
		userSelectString += "[" + strings.Join(userSelect, ", ") + "]\n\n"
	}
	err1 := sendDingDingNotification(hookUrl, drawPeriod, drawTime, hitPrizeArray, drawNum, userSelectString)
	if err1 != nil {
		fmt.Println("Error:", err1)
	}
}

func main() {
	// 启动则运行一次，给全局变量赋值
	run()
	// 创建一个cron调度器
	c := cron.New()

	// 添加定时任务
	_, err := c.AddFunc("*/1 21-23 * * 1,3,6", run)
	if err != nil {
		fmt.Println("添加定时任务失败：", err)
		return
	}

	// 启动定时任务
	c.Start()

	// 定时任务持续执行
	select {}
}
