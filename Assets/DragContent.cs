using UnityEngine;

public class DragContent : MonoBehaviour
{
    public Transform content;
    float offset;
    bool dragging = false;
    public float lerpSpeed = 10;

    public void StartDrag()
    {
        Vector3 inputPosition;
#if UNITY_EDITOR
        inputPosition = Input.mousePosition;
#else
        if (Input.touchCount == 0)
            return;
        inputPosition = Input.GetTouch(0).position;
#endif

        offset = content.position.y - inputPosition.y;
        dragging = true;
    }

    public void EndDrag()
    {
        dragging = false;
    }

    void Update()
    {
        if (dragging)
        {
            Drag();
        }   
    }

    void Drag()
    {
        Vector3 inputPosition;
#if UNITY_EDITOR
        inputPosition = Input.mousePosition;
#else
        if (Input.touchCount == 0)
            return;
        inputPosition = Input.GetTouch(0).position;
#endif
        content.position = Vector3.Lerp(content.position, new Vector3(content.position.x, Mathf.Min(inputPosition.y + offset, 0)), 
                                        lerpSpeed * Time.deltaTime);
    }
}
