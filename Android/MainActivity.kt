package com.example.testtaquincompose

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.core.LinearOutSlowInEasing
import androidx.compose.animation.core.animateIntOffsetAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.livedata.observeAsState
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.testtaquincompose.ui.theme.TestTaquinComposeTheme
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import java.util.Arrays
import kotlin.math.roundToInt

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            TestTaquinComposeTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    TaquinGrid(
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}


@Composable
fun TaquinGrid(
    modifier: Modifier = Modifier,
    viewModel: TaquinViewModel = viewModel()
) {

        for (element in taquinArray.value?: listOf()) {
            if (element == (taquinArray.value?: listOf()).size - 1) {
                continue
            }
            val xPosition = with(LocalDensity.current) {
                viewModel.getXPosition(element).dp.toPx().roundToInt()
            }
            val yPosition = with(LocalDensity.current) {
                viewModel.getYPosition(element).dp.toPx().roundToInt()
            }
            val offset by animateIntOffsetAsState(
                IntOffset(xPosition, y = yPosition),
                animationSpec = tween(
                    durationMillis = 3000,
                    easing = LinearOutSlowInEasing
                )
            )
            Button(
                onClick = { viewModel.tapHandler(element) },
                modifier = modifier
                    .offset { offset }
            ) {
                Text(viewModel.getText(element))
            }
        }
    }
}

class TaquinViewModel: ViewModel() {

    val arrayWidth: Int = 3
    val arrayHeight: Int = 3
    private val _currentArray = MutableLiveData<List<Int>>()
    val currentArray: LiveData<List<Int>> get() = _currentArray

    init {
        var testArray = List(arrayWidth * arrayHeight) { it }.shuffled()
        while (!possibleToSolve(testArray, arrayWidth, arrayHeight)) {
            testArray = testArray.shuffled()
        }
        _currentArray.value = testArray

    }

    fun possibleToSolve(array: List<Int>, arrayWidth: Int, arrayHeight: Int): Boolean {
        var count = 0
        val testArray = mutableListOf<Int>()
        for ((index, value) in array.withIndex()) {
            testArray += value
            if (value == array.size - 1) {
                count = arrayWidth + arrayHeight - (index % arrayWidth) - (index / arrayWidth)
            }
        }
        for (i in 0..<array.size) {
            if (testArray[i] != i) {
                for (j in i ..<array.size) {
                    if (testArray[j] == i) {
                        testArray[j] = testArray[i]
                        testArray[i] = i
                        count++
                    }
                }
            }
        }
        return count%2 == 0
    }

    fun getXPosition(element: Int): Int {
        val index = currentArray.value?.indexOf(element) ?: 0
        val xValue = index%arrayWidth
        return 100 + 75*xValue
    }

    fun getYPosition(element: Int): Int {
        val index = currentArray.value?.indexOf(element) ?: 0
        val yValue = index/arrayWidth
        return 100 + 75*yValue
    }

    fun getText(element: Int): String {
        if (element == (currentArray.value?.size ?: 0) - 1) {
            return ""
        }
        return "${element+1}"
    }

    fun tapHandler(element: Int) {
        val tempArray = (_currentArray.value ?: mutableListOf()).toMutableList()
        if (tempArray.isEmpty()) {
            return
        }
        val index = tempArray.indexOf(element)
        val xValue = index%arrayWidth
        val yValue = index/arrayWidth
        val blankValue = tempArray.size - 1
        if (xValue > 0 && tempArray[index-1] == blankValue) {
            tempArray[index-1] = element
            tempArray[index] = blankValue
        }
        if (xValue < arrayWidth - 1 && tempArray[index+1] == blankValue) {
            tempArray[index+1] = element
            tempArray[index] = blankValue
        }
        if (yValue > 0 && tempArray[index-arrayWidth] == blankValue) {
            tempArray[index-arrayWidth] = element
            tempArray[index] = blankValue
        }
        if (yValue < arrayHeight - 1 && tempArray[index+arrayWidth] == blankValue) {
            tempArray[index+arrayWidth] = element
            tempArray[index] = blankValue
        }
        _currentArray.postValue(tempArray)

    }
}
