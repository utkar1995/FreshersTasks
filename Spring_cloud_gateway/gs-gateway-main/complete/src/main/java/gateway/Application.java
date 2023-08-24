package gateway;

import reactor.core.publisher.Mono;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

// tag::code[]
@SpringBootApplication
//@EnableConfigurationProperties(UriConfiguration.class)

public class Application {

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}

	
	@Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("students_route", r -> r.path("/getAllStudents")
                .uri("http://localhost:9091/faculty/getAllStudents"))
            // Add more routes here
            .build();
    }
	// end::route-locator[]

//	// tag::fallback[]
//	@RequestMapping("/fallback")
//	public Mono<String> fallback() {
//		return Mono.just("fallback");
//	}
	// end::fallback[]
}

