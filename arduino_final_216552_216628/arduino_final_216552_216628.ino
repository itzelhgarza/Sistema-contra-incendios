#include <Bounce2.h>
#include <Config.h>
#include <EasyBuzzer.h>
#include <Servo.h>

int sensorLlama = 0;
int buzzer = 11;
Servo servoMotor;
int TRIG = 5;
int ECO = 4;
int TRIG2 = 6;
int ECO2 = 7;
int BOTON = 13;
int Duracion;
int Distancia;
int Duracion2;
int Distancia2;

Bounce debouncer = Bounce();

boolean statusEntrada = false;
boolean statusSalida = false;

int limiteTemperatura = 100;
int frecuencia = 200;
int valBoton;

int aux = 1;
int personas=0;

//Cosas del botón
const int pinon = 8;
boolean incendioMenorActivado = false;
boolean incendioMayorActivado = true;
int estaon= LOW;

void setup(){  
  servoMotor.write(0); 
  pinMode(sensorLlama,INPUT);
  pinMode(buzzer, OUTPUT);  
  servoMotor.attach(9);
  EasyBuzzer.setPin(buzzer);
  pinMode(TRIG, OUTPUT);
  pinMode(ECO, INPUT);
  pinMode(TRIG2, OUTPUT);
  pinMode(ECO2, INPUT);

  pinMode(pinon, INPUT);
  
  //pinMode(BOTON, INPUT);
  //BOTON = LOW;
  //debouncer.attach(BOTON);
  //debouncer.interval(10);
  
  
  Serial.begin(9600);  
} 
void loop(){
  //Serial.println(analogRead(A0)); 
  //debouncer.update();
  //if(debouncer.fell()){   
  //  Serial.println("Daisy WH");
  // decidirIncendio();    
  //  EasyBuzzer.stopBeep();
  //}
  boton();
  sensoresUltrasonicos();
  sistemaIncendio();
}
void boton(){
  estaon = digitalRead(pinon);
  if(estaon == HIGH){
    decidirIncendio();
  }
}
void decidirIncendio(){
  if(incendioMayorActivado == true and incendioMenorActivado == false){
    setIncendioMenor();
  }else if(incendioMenorActivado == true and incendioMayorActivado == false){
    setIncendioMayor();
  }
}
void setIncendioMayor(){
  limiteTemperatura = 100;
  frecuencia = 200;
  //aux = 1;
  incendioMayorActivado = true;
  incendioMenorActivado = false;
  Serial.println("7");
  delay(2000);
}
void setIncendioMenor(){
  limiteTemperatura = 135;
  frecuencia = 50;
  //aux = 2;
  incendioMenorActivado = true;
  incendioMayorActivado = false;
  Serial.println("6");
  delay(3000);
}
void sistemaIncendio(){
   sensorLlama = analogRead(A0);
   //Serial.println(sensorLlama);  
  if(sensorLlama <= limiteTemperatura){   
    EasyBuzzer.beep(frecuencia,5);
    servoMotor.write(180);
    Serial.println("1");
    delay(3000);
   } else{
    //Serial.println();
    EasyBuzzer.stopBeep();
    servoMotor.write(0);
    Serial.println("3");
   } 
}
void sensoresUltrasonicos(){
   detectarDE();
   detectarDS();
}

void detectarDE(){
  digitalWrite(TRIG, HIGH);
  delay(1);
  digitalWrite(TRIG, LOW);
  Duracion = pulseIn(ECO, HIGH);
  Distancia = Duracion / 58.2;
  if(Distancia < 5){
    esEntrada();
  }
}
void detectarDS(){
  digitalWrite(TRIG2, HIGH);
  delay(1);
  digitalWrite(TRIG2, LOW);
  Duracion2 = pulseIn(ECO2, HIGH);
  Distancia2 = Duracion2 / 58.2;
  if(Distancia2 < 5){
    esSalida();
  }
}
void esEntrada(){
  if(statusEntrada == false and statusSalida == false){
    statusEntrada = true;
    Serial.println("4");
    delay(1000);
  }else{
    reiniciar();
  }
}
void esSalida(){
  if(statusEntrada == false and statusSalida == false){
    statusSalida = true;
    Serial.println("5");
    delay(1000);
  }else{
    reiniciar();
  }
}
void reiniciar(){
  statusEntrada = false;
  statusSalida = false;
}
