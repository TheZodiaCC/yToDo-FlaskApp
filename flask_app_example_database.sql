
CREATE TABLE `things` (
  `thing_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `users` (
  `user_id` int(5) NOT NULL,
  `nick` varchar(20) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `back_code` varchar(20) NOT NULL,
  `saw_code` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `things`
  ADD PRIMARY KEY (`thing_id`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

ALTER TABLE `things`
  MODIFY `thing_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;
--
ALTER TABLE `users`
  MODIFY `user_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;
COMMIT;

