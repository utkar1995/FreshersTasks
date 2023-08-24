package com.radisys.restapi.model;

import jakarta.validation.constraints.NotEmpty;

//import javax.persistence.Column;
////import javax.persistence.Entity;
//import javax.persistence.GeneratedValue;
//import javax.persistence.GenerationType;
//import javax.persistence.Id;
//import javax.persistence.Table;
//import javax.validation.constraints.NotEmpty;
//import javax.validation.constraints.NotNull;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.Valid;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
//@Entity
//@Table(name = "student")
@Schema(accessMode = Schema.AccessMode.READ_ONLY)
@Document(collection = "Student")
public class Student {

	
	
	@Id
	Long rollNo;

	@NotEmpty(message = "Name can't be empty")
	
	String name;

	@NotNull(message = "age can't be empty")
	
	int age;
	@NotEmpty(message = "ph no can't be empty")
	
String phNo;
	@NotNull(message = "percentage can't be empty")

	float percentage;
@NotEmpty(message = "class can't be empty")


String class_;
int rank;
}
