package com.example.moodmusic

import android.content.Context
import android.media.MediaPlayer
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import com.example.moodmusic.ui.theme.MoodMusicTheme
import okhttp3.*
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.util.concurrent.TimeUnit

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MoodMusicTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    MoodMusicScreen(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(innerPadding)
                            .padding(24.dp)
                    )
                }
            }
        }
    }
}

@Composable
fun MoodMusicScreen(modifier: Modifier = Modifier) {
    var mood by remember { mutableStateOf(TextFieldValue("")) }
    var responseText by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var audioFilePath by remember { mutableStateOf<String?>(null) }
    val context = LocalContext.current
    val mediaPlayer = remember { MediaPlayer() }

    Column(
        modifier = modifier,
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Mood Music Generator",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 24.dp)
        )

        OutlinedTextField(
            value = mood,
            onValueChange = { mood = it },
            label = { Text("Enter your mood") },
            modifier = Modifier.fillMaxWidth(),
            enabled = !isLoading
        )

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {
                isLoading = true
                responseText = "Generating music..."
                generateMusicFromMood(context, mood.text) { result ->
                    responseText = result
                    isLoading = false
                    if (result == "Music downloaded!") {
                        audioFilePath = File(context.filesDir, "${mood.text}.wav").absolutePath
                    }
                }
            },
            enabled = !isLoading
        ) {
            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = MaterialTheme.colorScheme.onPrimary,
                    strokeWidth = 2.dp
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("Generating...")
            } else {
                Text("Generate Music")
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text(text = responseText)

        audioFilePath?.let { path ->
            Spacer(modifier = Modifier.height(16.dp))
            IconButton(
                onClick = {
                    try {
                        mediaPlayer.reset()
                        mediaPlayer.setDataSource(path)
                        mediaPlayer.prepare()
                        mediaPlayer.start()
                        Toast.makeText(context, "Playing music...", Toast.LENGTH_SHORT).show()
                    } catch (e: Exception) {
                        e.printStackTrace()
                        Toast.makeText(context, "Error playing audio: ${e.message}", Toast.LENGTH_LONG).show()
                    }
                }
            ) {
                Icon(Icons.Filled.PlayArrow, contentDescription = "Play Music")
            }
        }
    }
}

fun generateMusicFromMood(context: Context, mood: String, onDone: (String) -> Unit) {
    val client = OkHttpClient.Builder()
        .connectTimeout(1, TimeUnit.MINUTES)
        .writeTimeout(1, TimeUnit.MINUTES)
        .readTimeout(5, TimeUnit.MINUTES)
        .build()

    val moodEncoded = java.net.URLEncoder.encode(mood, "UTF-8")
    val url = "https://9678b21dc45d.ngrok-free.app/generate_music/?mood=$moodEncoded"

    val request = Request.Builder()
        .url(url)
        .get()
        .build()

    Toast.makeText(context, "Generating music for mood: $mood...", Toast.LENGTH_LONG).show()

    client.newCall(request).enqueue(object : Callback {
        override fun onFailure(call: Call, e: IOException) {
            e.printStackTrace()
            (context as ComponentActivity).runOnUiThread {
                Toast.makeText(context, "Network error: ${e.message}", Toast.LENGTH_LONG).show()
            }
            onDone("Network error: ${e.message}")
        }

        override fun onResponse(call: Call, response: Response) {
            if (response.isSuccessful) {
                val inputStream = response.body?.byteStream()
                val file = File(context.filesDir, "$mood.wav")
                val outputStream = FileOutputStream(file)

                inputStream?.copyTo(outputStream)
                outputStream.close()
                inputStream?.close()

                (context as ComponentActivity).runOnUiThread {
                    Toast.makeText(context, "Saved to ${file.absolutePath}", Toast.LENGTH_LONG).show()
                }
                onDone("Music downloaded!")
            } else {
                onDone("Error: ${response.code}")
            }
        }
    })
}
