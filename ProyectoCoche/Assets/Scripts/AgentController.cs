using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Agents
{
    public List<Vector3> positions;
}
public class AgentController : MonoBehaviour
{
    [SerializeField] string url;
    [SerializeField] string configEP;
    [SerializeField] string updateEP;
    [SerializeField] int numAgents;
    [SerializeField] GameObject carPrefab;
    [SerializeField] float updateDelay;
    Agents agents;
    GameObject[] cars;
    float updateTime = 0;

    // Start is called before the first frame update
    void Start()
    {
        cars = new GameObject[numAgents];
        for (int i = 0; i < numAgents; i++){
            cars[i] = Instantiate(carPrefab, Vector3.zero, Quaternion.identity);
        }
        StartCoroutine(SendConfiguration());
    }

    // Update is called once per frame
    void Update()
    {
        if(updateTime > updateDelay){
            StartCoroutine(UpdatePositions());
            updateTime = 0;
        }
        updateTime += Time.deltaTime;
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
            Debug.Log(www.downloadHandler.text);
            agents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);
            MoveCars();
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();
        form.AddField("numAgents", numAgents.ToString());
        UnityWebRequest www = UnityWebRequest.Post(url + configEP, form);
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        } else {
            Debug.Log(www.error);
        }
    }

    void MoveCars()
    {
        for(int i = 0; i < numAgents; i++){
            cars[i].transform.position = agents.positions[i];
        }
    }
}
