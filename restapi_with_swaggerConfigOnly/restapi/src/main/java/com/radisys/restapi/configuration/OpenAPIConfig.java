package com.radisys.restapi.configuration;

import java.util.Arrays;
import java.util.Collections;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import springfox.documentation.builders.AuthorizationCodeGrantBuilder;
import springfox.documentation.builders.OAuthBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.builders.TokenEndpointBuilder;
import springfox.documentation.builders.TokenRequestEndpointBuilder;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.AuthorizationScope;
import springfox.documentation.service.Contact;
import springfox.documentation.service.OAuth;
import springfox.documentation.service.SecurityReference;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spi.service.contexts.SecurityContext;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@Configuration
@EnableSwagger2
public class OpenAPIConfig {

	@Bean
    public Docket api() { 
        return new Docket(DocumentationType.SWAGGER_2)
		  .groupName("Student API")
          .select()                                  
          .apis(RequestHandlerSelectors.basePackage("com.radisys.restapi.controller1"))              
          .paths(PathSelectors.regex("/student/.*"))                          
          .build().apiInfo(getApiInfo());                                           
    }
	
	@Bean
    public Docket apiMarks() { 
        return new Docket(DocumentationType.SWAGGER_2)
		  .groupName("Student marks API")
          .select()                                  
          .apis(RequestHandlerSelectors.basePackage("com.radisys.restapi.controller1"))              
          .paths(PathSelectors.regex("/marks/.*"))                          
          .build().apiInfo(getApiInfo()).securitySchemes(Arrays.asList(securityScheme()))
          .securityContexts(Arrays.asList(securityContext()));                                     
    }
	private AuthorizationScope[] scopes() {
        return new AuthorizationScope[] {
            new AuthorizationScope("read", "Read Access"),
            new AuthorizationScope("write", "Write Access")
        };
    }
    private OAuth securityScheme() {
        return new OAuthBuilder()
            .name("spring_oauth")
            .grantTypes(Arrays.asList(new AuthorizationCodeGrantBuilder()
                .tokenEndpoint(new TokenEndpointBuilder().url("/oauth/token").build())
                .tokenRequestEndpoint(new TokenRequestEndpointBuilder().url("/oauth/authorize1").build())
                .build()))
            .scopes(Arrays.asList(scopes()))
            .build();
    }

    

    private SecurityContext securityContext() {
        return SecurityContext.builder()
            .securityReferences(Arrays.asList(new SecurityReference("spring_oauth", scopes())))
            .forPaths(PathSelectors.any())
            .build();
    }
	
	@Bean
    public Docket testAPI(){
        Docket tDocket = new Docket(DocumentationType.SWAGGER_2)
            .groupName("Faculty API")
            .select()
            .apis(RequestHandlerSelectors.basePackage("com.radisys.restapi.controller2"))
            .paths(PathSelectors.any())
            .build()
            
            .apiInfo(getApiInfo());
       
        return tDocket;
    }
	
	private ApiInfo getApiInfo() {
        return new ApiInfo(
                "Contact Application API",
                "This is a sample Spring Boot RESTful service using SpringFox + Swagger 2",
                "V1",
                "urn:tos",
                new Contact("Utkarsha", "https://www.dariawan.com", "uhajare@radisys.com"),
                "CC BY-SA 3.0",
                "https://creativecommons.org/licenses/by-sa/3.0/",
                Collections.emptyList()
        );
    }
}
