package com.radisys.restapi.controller;

import java.util.Collection;
//import java.util.Objects;

//import javax.validation.Valid;
//import javax.validation.constraints.NotNull;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.radisys.restapi.model.ErrorFormat;
import com.radisys.restapi.model.Student;
import com.radisys.restapi.model.UpdateStudentFormat;
import com.radisys.restapi.repository.StudentRepository;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;

@Tag(name = "CRUD", description = "CRUD by MongoDB management APIs")
@CrossOrigin(origins = "http://localhost:9091") // added for swagger-documentation purpose in order to test all URLS
@RequestMapping("/student")
@RestController
public class StudentController {

	@Autowired
	StudentRepository studentRepository;

	@Operation(summary = "Create a new Student", tags = { "Create" })
	@ApiResponses({
			@ApiResponse(responseCode = "201", content = {
					@Content(schema = @Schema(implementation = Student.class), mediaType = "application/json") }),
			@ApiResponse(responseCode = "500", content = { @Content(schema = @Schema()) }) })

	@PostMapping(value = "/student", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
	ResponseEntity<Student> createStudent(@RequestBody  @Valid Student student) {
		

		return ResponseEntity.ok(studentRepository.save(student));

	}
	
	

	@Operation(summary = "Retrieve a Student by Id", description = "Get a Student object by specifying its id. The response is Tutorial object with id, title, description and published status.", tags = {
			"Read" })
	@ApiResponses({
			@ApiResponse(responseCode = "200", content = {
					@Content(schema = @Schema(implementation = Student.class), mediaType = "application/json") }),
			@ApiResponse(responseCode = "404", content = { @Content(schema = @Schema(implementation = ErrorFormat.class)) }),
			@ApiResponse(responseCode = "500", content = { @Content(schema = @Schema(implementation = ErrorFormat.class)) }) })
	@GetMapping(value = "/student", produces = MediaType.APPLICATION_JSON_VALUE)
	ResponseEntity<Student> getStudentsById(
			@RequestParam(name = "roll") @NotNull(message = "Roll can't be empty or null") Long roll) {

		Student student = studentRepository.findById(roll)
				.orElseThrow(() -> new RuntimeException("Invalid RollNo : " + roll));
		return ResponseEntity.ok(student);

	}
	

	@Operation(summary = "Retrieve all Students", tags = { "Read" })
	@ApiResponses({
			@ApiResponse(responseCode = "200", content = {
					@Content(schema = @Schema(implementation = Student.class), mediaType = "application/json") }),
			@ApiResponse(responseCode = "204", description = "There are no Students", content = {
					@Content(schema = @Schema(implementation = ErrorFormat.class)) }),
			@ApiResponse(responseCode = "500", content = {
					@Content(schema = @Schema(implementation = ErrorFormat.class)) }) })

	@GetMapping(value = "/students", produces = MediaType.APPLICATION_JSON_VALUE)
	ResponseEntity<Collection<Student>> getAllStudents() {

		return ResponseEntity.ok(studentRepository.findAll());

	}
	
	
		
	

	@Operation(summary = "Delete a Student by Id", tags = { "Delete" })
	@ApiResponses({ @ApiResponse(responseCode = "204", content = { @Content(schema = @Schema(implementation = ErrorFormat.class)) }),
			@ApiResponse(responseCode = "500", content = { @Content(schema = @Schema()) }) })
	@DeleteMapping(value = "/student", produces = MediaType.APPLICATION_JSON_VALUE)
	ResponseEntity<Void> deleteStudentsById(
			@RequestParam(name = "roll") @NotNull(message = "Roll can't be empty or null") Long roll) {

		studentRepository.deleteById(roll);
		return ResponseEntity.accepted().build();

	}
	
	@Operation(summary = "Update a Student by Id", tags = { "Update" })
	@ApiResponses({
			@ApiResponse(responseCode = "200", content = {
					@Content(schema = @Schema(implementation = UpdateStudentFormat.class), mediaType = "application/json") }),
			@ApiResponse(responseCode = "500", content = { @Content(schema = @Schema(implementation = ErrorFormat.class)) }),
			@ApiResponse(responseCode = "404", content = { @Content(schema = @Schema(implementation = ErrorFormat.class)) }) })

	@PutMapping(value = "/student", produces = MediaType.APPLICATION_JSON_VALUE)
	ResponseEntity<Void> updateStudentsById(
			@RequestBody Student student) {

//		Student student = studentRepository.findById(roll).orElseThrow(() -> new RuntimeException("Invalid RollNo : " + roll));
		Long roll = student.getRollNo();
		Student existing_record = studentRepository.findById(roll)
				.orElseThrow(() -> new RuntimeException("Invalid RollNo : " + roll));
		existing_record.setName(student.getName());
		existing_record.setRank(student.getRank());
		studentRepository.save(existing_record);
		return ResponseEntity.accepted().build();

	}
}
