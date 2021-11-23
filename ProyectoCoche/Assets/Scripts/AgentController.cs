using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Agents
{
    public List<Vector3> positions;
    public List<int> objType;
}

public class RunHandler
{
    public string message;
}
public class AgentController : MonoBehaviour
{
    [SerializeField] string url;
    [SerializeField] string configEP;
    [SerializeField] string updateEP;
    [SerializeField] string robotEP;
    [SerializeField] string boxEP;
    [SerializeField] int numAgents;
    [SerializeField] GameObject robotPrefab;
    [SerializeField] GameObject boxPrefab;
    [SerializeField] float updateDelay;
    [SerializeField] int gridWidth;
    [SerializeField] int gridHeight;
    [SerializeField] int numBoxes;
    Agents agents;
    GameObject[] robots;
    GameObject[] boxes;
    float updateTime = 0;
    bool isFinished = false;
    int finishCounter = 5;

    // Start is called before the first frame update
    void Start()
    {
        robots = new GameObject[numAgents];
        for (int i = 0; i < numAgents; i++){
            robots[i] = Instantiate(robotPrefab, Vector3.zero, Quaternion.identity);
        }
        boxes = new GameObject[numBoxes];
        for (int i = 0; i < numBoxes; i++){
            boxes[i] = Instantiate(boxPrefab, Vector3.zero, Quaternion.identity);
        }
        StartCoroutine(SendConfiguration());
    }

    // Update is called once per frame
    void Update()
    {   
            if(!isFinished || finishCounter > 0){
                Debug.Log("Entered update");
                if(updateTime > updateDelay){
                    StartCoroutine(UpdatePositions());
                    StartCoroutine(UpdateRobotPositions());
                    StartCoroutine(UpdateBoxPositions());
                    updateTime = 0;
                }
                updateTime += Time.deltaTime;
            }
            if(isFinished){finishCounter -= 1;}
    }

    IEnumerator TestAPI()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + "/");
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator UpdatePositions()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            //Debug.Log(www.downloadHandler.text);
            RunHandler handler = JsonUtility.FromJson<RunHandler>(www.downloadHandler.text);
            if(handler.message == "Finished"){
                isFinished = true;
            }
        } else {
            Debug.Log(www.error);
        }
    }
    IEnumerator UpdateRobotPositions()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + robotEP);
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            //Debug.Log(www.downloadHandler.text);
            agents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);
            MoveRobots();
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator UpdateBoxPositions()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + boxEP);
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
            agents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);
            MoveBoxes();
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();
        form.AddField("numAgents", numAgents.ToString());
        form.AddField("gridWidth", gridWidth.ToString());
        form.AddField("gridHeight", gridHeight.ToString());
        form.AddField("numBoxes", numBoxes.ToString());
        UnityWebRequest www = UnityWebRequest.Post(url + configEP, form);
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        } else {
            Debug.Log(www.error);
        }
    }

    void MoveRobots()
    {
        for(int i = 0; i < numAgents; i++){
            robots[i].transform.position = agents.positions[i];
        }
    }

    void MoveBoxes()
    {
        for(int i = 0; i < numBoxes; i++){
            boxes[i].transform.position = agents.positions[i];
        }
    }
}
