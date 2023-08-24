package com.radisys.restapi.controller2;

import java.util.Collection;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.radisys.restapi.model.Student;
import com.radisys.restapi.repository.StudentRepository;

import springfox.documentation.swagger2.annotations.EnableSwagger2;

@EnableSwagger2
@RequestMapping("/faculty")
@RestController
public class FacultyController {

	@Autowired
	StudentRepository studentRepository;


	@PostMapping(value = "/createStudent", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
	ResponseEntity<Student> createStudent(@RequestBody  @Valid Student student) {
		

		return ResponseEntity.ok(studentRepository.save(student));

	}
	
	

		@GetMapping(value = "/getStudentsById", produces = MediaType.APPLICATION_JSON_VALUE)
	ResponseEntity<Student> getStudentsById(
			@RequestParam(name = "roll") @NotNull(message = "Roll can't be empty or null") Long roll) {

		Student student = studentRepository.findById(roll)
				.orElseThrow(() -> new RuntimeException("Invalid RollNo : " + roll));
		return ResponseEntity.ok(student);

	}
	

	
	@GetMapping(value = "/getAllStudents", produces = MediaType.APPLICATION_JSON_VALUE)
	ResponseEntity<Collection<Student>> getAllStudents() {

		return ResponseEntity.ok(studentRepository.findAll());

	}
	
	
		
	

		@DeleteMapping(value = "/deleteStudentsById", produces = MediaType.APPLICATION_JSON_VALUE)
	ResponseEntity<Void> deleteStudentsById(
			@RequestParam(name = "roll") @NotNull(message = "Roll can't be empty or null") Long roll) {

		studentRepository.deleteById(roll);
		return ResponseEntity.accepted().build();

	}
	
	
	@PutMapping(value = "/updateStudentsById", produces = MediaType.APPLICATION_JSON_VALUE)
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