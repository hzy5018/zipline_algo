language: PYTHON
name:     "BBANDS"

variable {
 name: "timeperiod"
 type: INT
 size: 1
 min:  10
 max:  25
}

variable {
 name: "nbdevup"
 type: FLOAT
 size: 1
 min:  0.50
 max:  2.50
}

variable {
 name: "nbdevdn"
 type: FLOAT
 size: 1
 min:  0.50
 max:  2.50
}
