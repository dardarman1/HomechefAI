using UnityEngine;

public class Capture : MonoBehaviour
{
    public void CaptureContent() {
        CameraFootage cameraFootage = FindAnyObjectByType<CameraFootage>();

        cameraFootage.DisableCamera();
    }
}
