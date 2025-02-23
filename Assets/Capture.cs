using UnityEngine;

public class Capture : MonoBehaviour
{
    public void CaptureContent() {
        CameraFootage cameraFootage = FindAnyObjectByType<CameraFootage>();

        byte[] imageBytes = ImageConversion.EncodeToPNG(cameraFootage.rawImage.texture);
        string base64Image = System.Convert.ToBase64String(imageBytes);
        string utf8Image = System.Text.Encoding.UTF8.GetString(System.Convert.FromBase64String(base64Image));

        cameraFootage.DisableCamera();
    }
}
