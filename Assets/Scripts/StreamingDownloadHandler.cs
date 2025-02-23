using UnityEngine;
using UnityEngine.Networking;
using System;
using System.Collections.Generic;

public class StreamingDownloadHandler : DownloadHandlerScript
{
    private List<byte> buffer = new List<byte>();
    private Action<string> onChunkReceived;

    // Delimiter for splitting chunks (e.g., "\n" or "\n\n")
    private string delimiter = "\n";

    public StreamingDownloadHandler(Action<string> onChunkReceived, string delimiter = "\n")
        : base(new byte[4096]) // Buffer size (adjust as needed)
    {
        this.onChunkReceived = onChunkReceived;
        this.delimiter = delimiter;
    }

    // Called every time new data is received
    protected override bool ReceiveData(byte[] incomingData, int dataLength)
    {
        if (incomingData == null || dataLength == 0)
            return false;

        // Add new bytes to the buffer
        for (int i = 0; i < dataLength; i++)
            buffer.Add(incomingData[i]);

        ProcessBuffer();
        return true;
    }

    private void ProcessBuffer()
    {
        // Convert buffer to string
        string bufferStr = System.Text.Encoding.UTF8.GetString(buffer.ToArray());

        // Split chunks by delimiter
        int lastDelimiterIndex = bufferStr.LastIndexOf(delimiter, StringComparison.Ordinal);
        if (lastDelimiterIndex == -1)
            return; // No complete chunk yet

        // Extract complete chunks
        string[] chunks = bufferStr.Substring(0, lastDelimiterIndex).Split(new[] { delimiter }, StringSplitOptions.RemoveEmptyEntries);

        // Remove processed bytes from the buffer
        int bytesProcessed = System.Text.Encoding.UTF8.GetByteCount(bufferStr.Substring(0, lastDelimiterIndex + delimiter.Length));
        buffer.RemoveRange(0, bytesProcessed);

        // Trigger callback for each chunk
        foreach (string chunk in chunks)
        {
            if (!string.IsNullOrEmpty(chunk))
                onChunkReceived?.Invoke(chunk.Trim());
        }
    }
}