const loadLeaderboard = (teams) => {
  //   console.log(team);

  teams.forEach((member) => {
    let newRow = document.createElement("li");
    newRow.classList = "c-list__item";
    newRow.innerHTML = `
		<div class="c-list__grid">
			<div class="c-flag c-place u-bg--transparent">${member.rank}</div>
			<div class="c-media">
				<div class="c-media__content">
					<div class="c-media__title">${member.user}</div>
				</div>
			</div>
			<div class="u-text--right">
                <strong>${member.ques_solved}</strong>
			</div>
            <div class="u-text--right c-points">
				<div class="u-mt--8">
					<strong>${member.score}</strong> ${randomEmoji()}
				</div>
			</div>
		</div>
	`;
    if (member.rank === 1) {
      newRow.querySelector(".c-place").classList.add("u-text--dark");
      newRow.querySelector(".c-place").classList.add("u-bg--yellow");
      newRow.querySelector(".c-points").classList.add("u-text--yellow");
    } else if (member.rank === 2) {
      newRow.querySelector(".c-place").classList.add("u-text--dark");
      newRow.querySelector(".c-place").classList.add("u-bg--teal");
      newRow.querySelector(".c-points").classList.add("u-text--teal");
    } else if (member.rank === 3) {
      newRow.querySelector(".c-place").classList.add("u-text--dark");
      newRow.querySelector(".c-place").classList.add("u-bg--orange");
      newRow.querySelector(".c-points").classList.add("u-text--orange");
    }
    list.appendChild(newRow);
  });
};

const randomEmoji = () => {
  const emojis = ["👏", "👍", "🙌", "🤩", "🔥", "⭐️", "🏆", "💯"];
  let randomNumber = Math.floor(Math.random() * emojis.length);
  return emojis[randomNumber];
};
